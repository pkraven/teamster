from __future__ import with_statement

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from utils.config import get_config


target_metadata = None
config = context.config
fileConfig(config.config_file_name)

app_config = get_config()
db_url = "{engine}://{user}:{password}@{host}:{port}/{database}".format(**app_config['db'])
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
