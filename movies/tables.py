import enum

from piccolo.columns import (
    Varchar,
    Boolean,
    JSON,
    Array,
    BigInt,
    Boolean,
    ForeignKey,
    Integer,
    Interval,
    Numeric,
    Real,
    SmallInt,
    Text,
    Timestamp,
    Varchar,
)
from piccolo.columns.readable import Readable
from piccolo.table import Table


class Director(Table, help_text="The main director for a movie."):
    class Gender(enum.Enum):
        male = "m"
        female = "f"
        non_binary = "n"

    name = Varchar(length=300, null=False)
    years_nominated = Array(
        base_column=Integer(),
        help_text=(
            "Which years this director was nominated for a best director "
            "Oscar."
        ),
    )
    gender = Varchar(length=1, choices=Gender)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Movie(Table):
    class Genre(int, enum.Enum):
        fantasy = 1
        sci_fi = 2
        documentary = 3
        horror = 4
        action = 5
        comedy = 6
        romance = 7
        musical = 8

    name = Varchar(length=300)
    rating = Real(help_text="The rating on IMDB.")
    duration = Interval()
    director = ForeignKey(references=Director)
    oscar_nominations = Integer()
    won_oscar = Boolean()
    description = Text()
    release_date = Timestamp(null=True)
    box_office = Numeric(digits=(5, 1), help_text="In millions of US dollars.")
    tags = Array(base_column=Varchar())
    barcode = BigInt(default=0)
    genre = SmallInt(choices=Genre, null=True)


class Studio(Table, help_text="A movie studio."):
    name = Varchar()
    facilities = JSON()


class Review(Table):
    name = Varchar()
    review = Text()
    score = Integer()
    movie = ForeignKey(Movie)
