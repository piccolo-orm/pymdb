from piccolo.apps.migrations.auto import MigrationManager
from enum import Enum
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import Array
from piccolo.columns.column_types import BigInt
from piccolo.columns.column_types import Boolean
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Interval
from piccolo.columns.column_types import JSON
from piccolo.columns.column_types import Numeric
from piccolo.columns.column_types import Real
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import SmallInt
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.interval import IntervalCustom
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table
import decimal


class Director(Table, tablename="director"):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
    )


class Movie(Table, tablename="movie"):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
    )


ID = "2021-10-28T22:40:09:258787"
VERSION = "0.58.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="movies", description=DESCRIPTION
    )

    manager.add_table("Review", tablename="review")

    manager.add_table("Director", tablename="director")

    manager.add_table("Task", tablename="task")

    manager.add_table("Studio", tablename="studio")

    manager.add_table("Movie", tablename="movie")

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="review",
        db_column_name="review",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="score",
        db_column_name="score",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Review",
        tablename="review",
        column_name="movie",
        db_column_name="movie",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Movie,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Director",
        tablename="director",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 300,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Director",
        tablename="director",
        column_name="years_nominated",
        db_column_name="years_nominated",
        column_class_name="Array",
        column_class=Array,
        params={
            "base_column": Integer(
                default=0,
                null=False,
                primary_key=False,
                unique=False,
                index=False,
                index_method=IndexMethod.btree,
                choices=None,
                db_column_name=None,
            ),
            "default": list,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Director",
        tablename="director",
        column_name="gender",
        db_column_name="gender",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 1,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Gender", {"male": "m", "female": "f", "non_binary": "n"}
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Task",
        tablename="task",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Task",
        tablename="task",
        column_name="completed",
        db_column_name="completed",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Studio",
        tablename="studio",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Studio",
        tablename="studio",
        column_name="facilities",
        db_column_name="facilities",
        column_class_name="JSON",
        column_class=JSON,
        params={
            "default": "{}",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 300,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="rating",
        db_column_name="rating",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="duration",
        db_column_name="duration",
        column_class_name="Interval",
        column_class=Interval,
        params={
            "default": IntervalCustom(
                weeks=0,
                days=0,
                hours=0,
                minutes=0,
                seconds=0,
                milliseconds=0,
                microseconds=0,
            ),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="director",
        db_column_name="director",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Director,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="oscar_nominations",
        db_column_name="oscar_nominations",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="won_oscar",
        db_column_name="won_oscar",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="description",
        db_column_name="description",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="release_date",
        db_column_name="release_date",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="box_office",
        db_column_name="box_office",
        column_class_name="Numeric",
        column_class=Numeric,
        params={
            "default": decimal.Decimal("0"),
            "digits": (5, 1),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="tags",
        db_column_name="tags",
        column_class_name="Array",
        column_class=Array,
        params={
            "base_column": Varchar(
                length=255,
                default="",
                null=False,
                primary_key=False,
                unique=False,
                index=False,
                index_method=IndexMethod.btree,
                choices=None,
                db_column_name=None,
            ),
            "default": list,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="barcode",
        db_column_name="barcode",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Movie",
        tablename="movie",
        column_name="genre",
        db_column_name="genre",
        column_class_name="SmallInt",
        column_class=SmallInt,
        params={
            "default": 0,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Genre",
                {
                    "fantasy": 1,
                    "sci_fi": 2,
                    "documentary": 3,
                    "horror": 4,
                    "action": 5,
                    "comedy": 6,
                    "romance": 7,
                    "musical": 8,
                },
            ),
            "db_column_name": None,
        },
    )

    return manager
