# tento súbor z veľkej časti generoval priamo Alembic, používa ho pre nadviazanie spojenia s databázou
# boli vykonané minimálne zmeny (napríklad, aby sa bralo `DATABASE_URL` priamo z env premennej)
# ...pre ďalšie info, kuk dokumentáciu: https://alembic.sqlalchemy.org/en/latest/tutorial.html

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from dotenv import load_dotenv
load_dotenv(override=True)

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))

# setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

try:
    from orm import Base  # noqa: E402
except ImportError:
    raise RuntimeError(
        "`orm.py` sa nenašlo – si v správnom priečinku (`cd backend/db`)?",
    )

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
