# app/migrations/env.py
import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine  # <-- sync engine

from app.core.config import settings
from app.db.base import Base

# PYTHONPATH к корню репо (чтобы импортировался пакет app)
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_sync_url() -> str:
    # Превращаем async URL в sync для Alembic
    url = settings.database_url
    # примеры:
    # postgresql+asyncpg:// -> postgresql+psycopg://
    return (
        url.replace("+asyncpg", "+psycopg")
        .replace("+aiopg", "+psycopg")
        .replace("+asyncpg", "")  # на случай пустого драйвера
    )


def run_migrations_offline():
    context.configure(
        url=get_sync_url(),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(get_sync_url(), future=True)
    with engine.begin() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
