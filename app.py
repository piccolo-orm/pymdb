import typing as t

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.serializers import create_pydantic_model
from piccolo_api.fastapi.endpoints import (
    FastAPIWrapper,
    PiccoloCRUD,
    FastAPIKwargs,
)
from pydantic.main import BaseModel
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

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


# If we were creating them by hand:
class ReviewModel(BaseModel):
    """
    This is OK, but becomes error prone and tedious when we have lots of
    columns.
    """

    name: str
    review: str
    score: int
    movie: int


# Using `create_pydantic_model` instead:
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
async def get_reviews():
    """
    Get all reviews.
    """
    return await Review.select().order_by(Review.id).run()


@app.get(
    "/reviews/{review_id}/",
    response_model=ReviewModelOut,
    tags=["Review"],
)
async def get_review(review_id: int):
    """
    Get a single review.
    """
    review = await Review.select().where(Review.id == review_id).first().run()
    if not review:
        return JSONResponse({}, status_code=404)

    return review


@app.post("/reviews/", response_model=ReviewModelOut, tags=["Review"])
async def create_review(review_model: ReviewModelIn):
    """
    Create a new review.
    """
    review = Review(**review_model.__dict__)
    await review.save().run()
    return review.to_dict()


@app.put(
    "/reviews/{review_id}/", response_model=ReviewModelOut, tags=["Review"]
)
async def replace_review(review_id: int, review_model: ReviewModelIn):
    """
    Replace an existing review.
    """
    review = await Review.objects().where(Review.id == review_id).first().run()
    if not review:
        return JSONResponse({}, status_code=404)

    for key, value in review_model.__dict__.items():
        setattr(review, key, value)

    await review.save().run()

    return review.to_dict()


@app.patch(
    "/reviews/{review_id}/", response_model=ReviewModelOut, tags=["Review"]
)
async def update_review(review_id: int, review_model: ReviewModelOptional):
    """
    Update a review.
    """
    review = await Review.objects().where(Review.id == review_id).first().run()
    if not review:
        return JSONResponse({}, status_code=404)

    for key, value in review_model.__dict__.items():
        if value is not None:
            setattr(review, key, value)

    await review.save().run()

    return review.to_dict()


@app.delete("/reviews/{review_id}/", tags=["Review"])
async def delete_review(review_id: int):
    """
    Delete a review.
    """
    review = await Review.objects().where(Review.id == review_id).first().run()
    if not review:
        return JSONResponse({}, status_code=404)

    await review.remove().run()

    return JSONResponse({})


###############################################################################
# Rather than defining the FastAPI endpoints by hand, we can use
# `FastAPIWrapper`, which can save us a lot of time.

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
