from ._example_data import DIRECTORS, MOVIES, STUDIOS
from movies.tables import Director, Movie, Studio


def load_data():
    """
    Load some example data into the database.
    """
    for table_class in [Movie, Studio, Director]:
        table_class.delete(force=True).run_sync()

    Director.insert(*[Director(**d) for d in DIRECTORS]).run_sync()
    Movie.insert(*[Movie(**m) for m in MOVIES]).run_sync()
    Studio.insert(*[Studio(**s) for s in STUDIOS]).run_sync()

    engine_type = Director._meta.db.engine_type

    if engine_type == "postgres":
        # We need to update the sequence, as we explicitly set the IDs for the
        # directors we just inserted
        Director.raw(
            "SELECT setval('director_id_seq', max(id)) FROM director"
        ).run_sync()
