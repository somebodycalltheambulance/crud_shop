from logging.config import fileConfig

from alembic import context

from app.core.config import settings
from app.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    import asyncio

    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(settings.database_url, pool_pre_ping=True)

    async def run_async():
        async with engine.begin() as conn:
            await conn.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn, target_metadata=target_metadata
                )
            )
            context.run_migrations()

    asyncio.run(run_async())
