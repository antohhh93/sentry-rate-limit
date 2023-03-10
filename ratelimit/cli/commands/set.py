import click
import logging

from ratelimit.limit import Limit
from ratelimit.db import (
    LimitDatabase,
    OrganizationProjectDatabase,
    ProjectKeyDatabase,
)

"""
set:
    проверяет организации в базе данных
    обновляет лимиты ключей в sentry
"""

logger = logging.getLogger()

@click.command()
def set():
    """Set the speed limit in sentry."""

    logger.info("Starting set.")

    objects = OrganizationProjectDatabase()
    objects.get_organizations()

    organizations = objects.organizations

    if all(not organization 
                for organization in organizations):
        logger.error("No data to set.")
        logger.info("Stopping set.")
        return

    objects.get_projects()
    objects.get_organization_projects()
    objects.creating_array_organization_and_projects()

    database_organizations_projects = objects.organization_list

    objects = Limit(
        database_limits = LimitDatabase().get_limit(),
        database_organizations_projects = database_organizations_projects,
        database_projects_keys = ProjectKeyDatabase().get_project_key(),
    )
    objects.update_limit_key_to_sentry()

    logger.info("Stopping set.")