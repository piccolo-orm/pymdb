from piccolo.apps.migrations.auto import MigrationManager


ID = "2021-10-29T13:32:39:202304"
VERSION = "0.58.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="movies", description=DESCRIPTION
    )

    manager.drop_table(class_name="Task", tablename="task")

    return manager
