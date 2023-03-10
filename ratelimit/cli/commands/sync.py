import click
import logging

from ratelimit.organization import Organization
from ratelimit.project import Project
from ratelimit.key import Key
from ratelimit.limit import Limit
from ratelimit.organization_project import OrganizationProject
from ratelimit.project_key import ProjectKey
from ratelimit.sentry import (
    OrganizationGetSentry,
    ProjectGetSentry,
    KeyGetSentry,
)
from ratelimit.db import (
    OrganizationDatabase,
    ProjectDatabase,
    KeyDatabase,
    LimitDatabase,
    OrganizationProjectDatabase,
    ProjectKeyDatabase,
)

"""
sync:
    проверяет организации в базе данных

sync.organization_sync:
    удаляет организации из базы данных, если их нет в senty

sync.project_sync:
    удаляет проекты из базы данных, если их нет в senty
    добавляет проекты из sentry в базу данных

sync.key_sync:
    удаляет ключи из базы данных, если их нет в senty
    добавляет ключи из sentry в базу данных

sync.organization_project_sync:
    создает зависимости между организациями и проектами в базе данных

sync.project_key_sync:
    создает зависимости между проектами и ключами в базе данных

sync.limit_to_project:
    обновляет лимиты в проектах без фиксированных значений

sync.limit_to_key:
    обновляет лимиты в ключах без фиксированных значений
"""

logger = logging.getLogger()

def organization_sync():
    """Update organizations in the database."""

    objects = Organization(
        sentry_organizations = OrganizationGetSentry().get_organizations(),
        database_organizations = OrganizationDatabase().get_organizations(),
    )
    objects.delete_organization_missing_in_sentry()

def project_sync():
    """Update projects in the database."""

    objects = Project(
        sentry_projects = ProjectGetSentry().get_projects(),
        database_projects = ProjectDatabase().get_projects(),
        database_organizations = OrganizationDatabase().get_organizations(),
    )
    objects.delete_project_missing_in_sentry()
    objects.create_project_in_database()

def key_sync():
    """Update keys in the database."""

    objects = OrganizationProjectDatabase()
    objects.get_organizations()
    objects.get_projects()
    objects.get_organization_projects()

    organizations_with_projects = objects.creating_array_organization_and_projects()

    objects = Key(
        sentry_keys = KeyGetSentry(
            organizations_with_projects = organizations_with_projects,
        ).get_project_keys(),
        database_keys = KeyDatabase().get_keys(),
        database_projects = OrganizationProjectDatabase().get_projects(),
    )
    objects.delete_key_missing_in_sentry()
    objects.create_new_key_in_database()

def organization_project_sync():
    """Update link organizations and projects in the database."""

    objects = OrganizationProject(
        sentry_projects = ProjectGetSentry().get_projects(),
        database_projects = ProjectDatabase().get_projects(),
        database_organizations = OrganizationDatabase().get_organizations(),
        database_organizations_projects = OrganizationProjectDatabase().get_organization_projects(),
    )
    objects.create_dependency_between_organization_and_project()

def project_key_sync():
    """Update link projects and keys in the database."""

    objects = OrganizationProjectDatabase()
    objects.get_organizations()
    objects.get_projects()
    objects.get_organization_projects()

    organizations_with_projects = objects.creating_array_organization_and_projects()

    objects = ProjectKey(
        sentry_keys = KeyGetSentry(
            organizations_with_projects = organizations_with_projects,
        ).get_project_keys(),
        database_keys = KeyDatabase().get_keys(),
        database_projects = ProjectKeyDatabase().get_projects(),
        database_projects_keys = ProjectKeyDatabase().get_project_key(),
    )
    objects.create_dependency_between_project_and_key()

def limit_to_project():
    """Updating projects limit."""

    objects = OrganizationProjectDatabase()
    objects.get_limit()
    objects.get_organizations()
    objects.get_projects()
    objects.get_organization_projects()
    objects.creating_array_organization_and_projects()

    organization_data = objects.organization_list

    objects = Limit(
        database_limits = LimitDatabase().get_limit(),
        database_organizations_projects = organization_data,
    )
    objects.update_limit_to_project()

def limit_to_key():
    """Updating keys limit."""

    objects = ProjectKeyDatabase()
    objects.get_limit()
    objects.get_projects()
    objects.get_keys()
    objects.get_project_key()
    objects.creating_array_project_and_key()

    project_data = objects.project_list

    objects = Limit(
        database_limits = LimitDatabase().get_limit(),
        database_projects_keys = project_data,
    )
    objects.update_limit_to_key()

@click.command()
@click.option(
    "-L", "--limit-only", "limit",
    is_flag=True,
    expose_value=True,
    help="Sync only limits."
)
@click.option(
    "-N", "--no-limit", "no_limit",
    is_flag=True,
    expose_value=True,
    help="Sync all except limits."
)
def sync(limit, no_limit):
    """Syncs data from Sentry."""

    logger.info("Starting sync.")

    objects = OrganizationDatabase()
    objects.get_organizations()

    if all(not organization 
                for organization in objects.organizations):
        logger.error("No data to sync.")
        logger.info("Stopping sync.")
        return

    if not limit:
        organization_sync()
        project_sync()
        organization_project_sync()
        key_sync()
        project_key_sync()

    if not no_limit:
        limit_to_project()
        limit_to_key()

    logger.info("Stopping sync.")
