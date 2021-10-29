import typing as t

from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.serializers import create_pydantic_model
from piccolo.engine import engine_finder
from starlette.routing import Route, Mount
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from movies.endpoints import HomeEndpoint
from movies.tables import Review
from movies.piccolo_app import APP_CONFIG

###############################################################################
# Create the FastAPI instance

app = FastAPI(
    routes=[
        Route("/", HomeEndpoint),
        Mount(
            "/admin/",
            create_admin(tables=APP_CONFIG.table_classes, site_name="PyMDB"),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)

###############################################################################
# Some Pydantic models

ReviewModelIn = create_pydantic_model(table=Review, model_name="ReviewModelIn")
ReviewModelOut = create_pydantic_model(
    table=Review, include_default_columns=True, model_name="ReviewModelOut"
)

###############################################################################
# Some traditional FastAPI endpoints


@app.get("/reviews/", response_model=t.List[ReviewModelOut])
async def reviews():
    return await Review.select().order_by(Review.id).run()


@app.post("/reviews/", response_model=ReviewModelOut)
async def create_review(task: ReviewModelIn):
    task = Review(**task.__dict__)
    await task.save().run()
    return ReviewModelOut(**task.__dict__)


@app.put("/reviews/{task_id}/", response_model=ReviewModelOut)
async def update_review(review_id: int, task: ReviewModelIn):
    _task = await Review.objects().where(Review.id == review_id).first().run()
    if not _task:
        return JSONResponse({}, status_code=404)

    for key, value in task.__dict__.items():
        setattr(_task, key, value)

    await _task.save().run()

    return ReviewModelOut(**_task.__dict__)


@app.delete("/reviews/{task_id}/")
async def delete_review(task_id: int):
    task = await Review.objects().where(Review.id == task_id).first().run()
    if not task:
        return JSONResponse({}, status_code=404)

    await task.remove().run()

    return JSONResponse({})


###############################################################################


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder()
    await engine.start_connection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connection_pool()
