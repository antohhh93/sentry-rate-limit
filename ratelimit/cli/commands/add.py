import click
import logging

from ratelimit.sentry import OrganizationGetSentry
from ratelimit.db import (
    model,
    Database,
    OrganizationDatabase,
)
from ratelimit.config import (
    DEFAULT_LIMIT_COUNT,
    DEFAULT_LIMIT_WINDOW,
)

"""
add.organization:
    проверяет добавляемую организацию в sentry
    проверяет добавляемую организацию в базе данных
    добавляет новый фиксированный лимит в базу данныз
    добавляет организацию в базу данных
"""

logger = logging.getLogger()

def organization(name, limit, desc):
    """Add an organization."""

    objects = OrganizationGetSentry()
    objects.get_organizations()

    if all(name.lower() != organization['slug'] 
                for organization in objects.organizations):
        logger.error("The [{0}] organization does not exist in sentry.".format(name))
        return

    organization_data = [organization for organization in objects.organizations if organization['slug'] == name.lower()][0]

    objects = OrganizationDatabase()
    objects.get_organizations()

    if any(organization_data['id'] == organization['organization_sentry_id'] 
                for organization in objects.organizations):
        logger.error("The [{0}] organization already exists in the database.".format(name))
        return

    count = limit if limit else DEFAULT_LIMIT_COUNT
    window = DEFAULT_LIMIT_WINDOW
    description = "Limit for the organization {0}. {1}".format(name, desc if desc else '')

    objects = Database()

    limit_id = objects.insert_one_row(model.Limit, 
                        count = count, 
                        window = window, 
                        description = description,
                        fixed = True
                    )

    if objects.insert_one_row(model.Organization, 
                        organization_sentry_id = organization_data['id'],
                        slug = organization_data['slug'],
                        limit_id = limit_id
                    ):
        logger.info("A new organization [{0}] has been created in the database.".format(name))
        return

@click.command()
@click.option(
    "-o", "--organization-name", "organization_name",
    type=str,
    required=False,
    expose_value=True,
    help="Organization name. Not display name."
)
@click.option(
    "-l", "--limit-count", "limit",
    type=int,
    required=False,
    expose_value=True,
    help="Limit count."
)
@click.option(
    "-d", "--desc", "desc",
    type=str,
    required=False,
    expose_value=True,
    help="Description."
)
def add(organization_name, limit, desc):
    """Add data to the database.

    Examples:

    \b
        $ sentry-rate-limit add --organization-name test --limit-count 300 --desc "Testing."
        $ sentry-rate-limit add --organization-name test --limit-count 300
        $ sentry-rate-limit add --organization-name test
    """

    logger.info("Starting add.")

    if organization_name:
        organization(
            name = organization_name, 
            limit = limit,
            desc = desc,
        )
    else:
        logger.error("There is not a single value to add.")

    logger.info("Stopping add.")