import click
import logging

from ratelimit.db import (
    models,
    Migrations
)

logger = logging.getLogger()

@click.command()
@click.pass_context
def init(ctx):
    "Initialize the tables in the database."

    logger.info("Starting init.")

    objects = Migrations()
    objects.create_all_tables(models)
    objects.apply_migration_limit()

    logger.info("Stopping init.")
