import click
import logging

from ratelimit.db import (
    model,
    Database,
    OrganizationDatabase,
)
"""
delete.organization:
    проверяет удаляемую организацию в базе данных
    удаляет организацию из базы данных
"""

logger = logging.getLogger()

def organization(name):
    """Delete an organization."""

    objects = OrganizationDatabase()
    objects.get_organizations()

    if all(name.lower() != organization['slug'] 
                for organization in objects.organizations):
        logger.error("The [{0}] organization does not exist in the database.".format(name.title()))
        return

    organization_data = [organization for organization in objects.organizations if organization['slug'] == name.lower()][0]

    objects = Database()

    if objects.recursive_delete_id(model.Organization, organization_data['id']):
        logger.info("The [{0}] organization removed from database.".format(name.title()))
        return

@click.command()
@click.option(
    "-o", "--organization-name", "organization_name",
    type=str,
    required=False,
    expose_value=True,
    help="Organization name. Not display name."
)
def delete(organization_name):
    """Delete data from the database.

    Examples:

    \b
        $ sentry-rate-limit delete --organization-name test
    """

    logger.info("Starting delete.")

    if organization_name:
        organization(
            name = organization_name,
        )
    else:
        logger.error("There is not a single value to delete.")

    logger.info("Stopping delete.")