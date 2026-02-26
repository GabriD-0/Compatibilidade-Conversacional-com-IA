import logging
from logging.config import fileConfig
from alembic import context
import sys
import os

# TODO: Reavaliar migrations

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from run import app
    app.app_context().push()
except Exception:
    pass

config = context.config
if config.config_file_name is not None and os.path.isfile(config.config_file_name):
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def get_engine():
    from flask import current_app
    try:
        return current_app.extensions["migrate"].db.get_engine()
    except (TypeError, AttributeError):
        return current_app.extensions["migrate"].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace("%", "%%")
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")


def get_metadata():
    from flask import current_app
    target_db = current_app.extensions["migrate"].db
    if hasattr(target_db, "metadatas"):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url", get_engine_url())
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    from flask import current_app
    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
