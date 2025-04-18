import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.database import db  # Import db SQLAlchemy instance
from app import create_app   # Import create_app

# Load config and models
app = create_app()
with app.app_context():
    target_metadata = db.metadata

config = context.config

# Override URL from Flask config
config.set_main_option(
    "sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"]
)

fileConfig(config.config_file_name)

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Agar perubahan tipe data juga terdeteksi
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
