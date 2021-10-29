import typing as t

from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.serializers import create_pydantic_model
from piccolo.engine import engine_finder
from starlette.routing import Route, Mount
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from piccolo_api.fastapi.endpoints import (
    FastAPIWrapper,
    PiccoloCRUD,
    FastAPIKwargs,
)

from movies.endpoints import HomeEndpoint
from movies.tables import Review, Movie
from movies.piccolo_app import APP_CONFIG

###############################################################################
# Create the FastAPI instance

app = FastAPI(
    routes=[
        Route("/", HomeEndpoint),
        Mount(
            "/admin/",
            create_admin(tables=APP_CONFIG.table_classes, site_name="PyMDb"),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)

###############################################################################
# Some Pydantic models

ReviewModelIn = create_pydantic_model(table=Review, model_name="ReviewModelIn")
ReviewModelOptional = create_pydantic_model(
    table=Review, model_name="ReviewModelOptional", all_optional=True
)
ReviewModelOut = create_pydantic_model(
    table=Review, include_default_columns=True, model_name="ReviewModelOut"
)

###############################################################################
# Some traditional FastAPI endpoints


@app.get("/reviews/", response_model=t.List[ReviewModelOut], tags=["Review"])
async def reviews():
    return await Review.select().order_by(Review.id).run()


@app.post("/reviews/", response_model=ReviewModelOut, tags=["Review"])
async def create_review(task: ReviewModelIn):
    task = Review(**task.__dict__)
    await task.save().run()
    return task.to_dict()


@app.put(
    "/reviews/{review_id}/", response_model=ReviewModelOut, tags=["Review"]
)
async def replace_review(review_id: int, task: ReviewModelIn):
    _task = await Review.objects().where(Review.id == review_id).first().run()
    if not _task:
        return JSONResponse({}, status_code=404)

    for key, value in task.__dict__.items():
        setattr(_task, key, value)

    await _task.save().run()

    return _task.to_dict()


@app.patch(
    "/reviews/{review_id}/", response_model=ReviewModelOut, tags=["Review"]
)
async def update_review(review_id: int, task: ReviewModelIn):
    _task = await Review.objects().where(Review.id == review_id).first().run()
    if not _task:
        return JSONResponse({}, status_code=404)

    for key, value in task.__dict__.items():
        if value is not None:
            setattr(_task, key, value)

    await _task.save().run()

    return _task.to_dict()


@app.delete("/reviews/{review_id}/", tags=["Review"])
async def delete_review(task_id: int):
    task = await Review.objects().where(Review.id == task_id).first().run()
    if not task:
        return JSONResponse({}, status_code=404)

    await task.remove().run()

    return JSONResponse({})


###############################################################################
# Rather than defining the FastAPI endpoints by hand, we can use
# FastAPIWrapper, which can save us a lot of time.

FastAPIWrapper(
    "/movies",
    fastapi_app=app,
    piccolo_crud=PiccoloCRUD(Movie, read_only=False),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["Movie"]},
    ),
)


###############################################################################
# Connection pool.


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder()
    await engine.start_connection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connection_pool()
