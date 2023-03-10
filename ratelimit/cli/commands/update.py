import click
import logging

from ratelimit.db import (
    Database,
    Organization,
    Project,
    Limit,
    Key,
    OrganizationDatabase,
    ProjectDatabase,
    LimitDatabase,
    KeyDatabase,
    OrganizationProjectDatabase,
    ProjectKeyDatabase,
)
from ratelimit.config import (
    DEFAULT_LIMIT_WINDOW,
    MIN_LIMIT_COUNT,
)


"""
update.limit:
    проверяет ключ в базе данных
    проверяет проект в базе данных
    проверяет организацию в базе данных

update.limit.checking_available_limit:
    проверяет доступные лимиты организации

update.limit.organization:
    проверяет обновляемую организацию в базе данных
    проверяет новый лимит с лимитом организации в базе данных
    добавляет новый фиксированный лимит в базу данных
    обновляет организацию в базе данных

update.limit.project:
    проверяет обновляемый проект в базе данных
    проверяет новый лимит с лимитом проекта в базе данных
    добавляет новый фиксированный лимит в базу данных
    обновляет проект в базе данных

update.limit.key:
    проверяет обновляемый ключ в базе данных
    проверяет новый лимит с лимитом ключа в базе данных
    добавляет новый фиксированный лимит в базу данных
    обновляет ключ в базе данных
"""

logger = logging.getLogger()

def checking_available_limit(organization, limit):
    fixed_project: list = []
    count_fixed_project: int = 0

    projects_count = len(organization['projects'])

    for project_data in organization['projects']:
        if project_data['limit_id']:
            if project_data['limit']['fixed']:
                fixed_project.append(project_data)

    count_fixed_project = len(fixed_project)
    sum_fixed_limit_project = sum(project_data['limit']['count'] for project_data in fixed_project)

    left_projects_count = ((projects_count - 1) - count_fixed_project)
    left_limit_organization = ((organization['limit']['count'] - limit) - sum_fixed_limit_project)
    left_limit_project = round(left_limit_organization / (left_projects_count if left_projects_count > 0 else 1))

    if left_projects_count > 0:
        if left_limit_project < MIN_LIMIT_COUNT:
            logger.error("The limit is not enough for other projects, increase the limit for the organization.")
            return False

    if left_projects_count == 0:
        if left_limit_project < 0:
            logger.error("The organization's available limit has been exceeded.")
            return False

    return True

def organization(organization_name, limit, desc):
    """Updating organization limit in the database."""

    objects = OrganizationDatabase()
    objects.get_organizations()

    if all(organization_name.lower() != organization['slug'] 
                for organization in objects.organizations):
        logger.error("The organization does not exist.")
        return

    organization_data = [organization_data for organization_data in objects.organizations if organization_data['slug'] == organization_name.lower()][0]

    objects = LimitDatabase()
    objects.get_limit()

    if (limit == [limit_data['count'] for limit_data in objects.limits if organization_data['limit_id'] == limit_data['id']][0]):
        logger.warning("This limit has already been set.")
        return

    count = limit
    window = DEFAULT_LIMIT_WINDOW
    description = "Limit for the organization {0}. {1}".format(organization_name, desc if desc else '')

    objects = Database()

    limit_id = objects.insert_one_row(Limit, 
                        count = count, 
                        window = window, 
                        description = description,
                        fixed = True
                    )

    if objects.update_limit(Organization, 
                        id = organization_data['id'], 
                        limit_id = limit_id
                    ):
        logger.info("The limit for the organization [{0}] have been updated.".format(organization_name))
        return

def project(project_name, organization_name, limit, desc):
    """Updating project limit in the database."""

    objects = OrganizationDatabase()
    objects.get_organizations()

    if all(organization_name.lower() != organization['slug'] 
                for organization in objects.organizations):
        logger.error("The organization does not exist.")
        return

    objects = ProjectDatabase()
    objects.get_projects()

    if all(project_name.lower() != project['slug'] 
                for project in objects.projects):
        logger.error("The project does not exist.")
        return

    objects = OrganizationProjectDatabase()
    objects.get_limit()
    objects.get_organizations()
    objects.get_projects()
    objects.get_organization_projects()
    objects.creating_array_organization_and_projects()

    organization_data = [organization_data for organization_data in objects.organization_list if organization_data['slug'] == organization_name.lower()][0]

    if all(project_name.lower() != project_data['slug'] 
                for project_data in organization_data['projects']):
        logger.error("The project does not exist in the organization.")
        return

    if not checking_available_limit(organization_data, limit):
        return
    
    project_data = [project_data for project_data in organization_data['projects'] if project_name.lower() == project_data['slug']][0]

    if (limit == [limit_data['count'] for limit_data in objects.limits if project_data['limit_id'] == limit_data['id']][0] and project_data['limit']['fixed']):
        logger.warning("This limit has already been set.")
        return

    count = limit
    window = DEFAULT_LIMIT_WINDOW
    description = "Limit for the project {0}. {1}".format(project_name, desc if desc else '')

    objects = Database()

    limit_id = objects.insert_one_row(Limit, 
                        count = count, 
                        window = window, 
                        description = description,
                        fixed = True
                    )

    if objects.update_limit(Project, 
                        id = project_data['id'], 
                        limit_id = limit_id
                    ):
        logger.info("The limit for the project [{0}] have been updated.".format(project_name))
        return

def key(public_key, project_name, organization_name, limit, desc):
    """Updating key limit in the database."""

    objects = OrganizationDatabase()
    objects.get_organizations()

    if all(organization_name.lower() != organization['slug'] 
                for organization in objects.organizations):
        logger.error("The organization does not exist.")
        return

    objects = ProjectDatabase()
    objects.get_projects()

    if all(project_name.lower() != project['slug'] 
                for project in objects.projects):
        logger.error("The project does not exist.")
        return

    objects = KeyDatabase()
    objects.get_keys()

    if all(public_key != key['key_sentry_id'] 
                for key in objects.keys):
        logger.error("The key does not exist.")
        return

    objects = OrganizationProjectDatabase()
    objects.get_limit()
    objects.get_organizations()
    objects.get_projects()
    objects.get_organization_projects()
    objects.creating_array_organization_and_projects()

    organization_data = [organization_data for organization_data in objects.organization_list if organization_data['slug'] == organization_name.lower()][0]

    if all(project_name.lower() != project_data['slug'] 
                for project_data in organization_data['projects']):
        logger.error("The project does not exist in the organization.")
        return

    objects = ProjectKeyDatabase()
    objects.get_limit()
    objects.get_projects()
    objects.get_keys()
    objects.get_project_key()
    objects.creating_array_project_and_key()

    project_data = [project_data for project_data in objects.project_list if project_data['slug'] == project_name.lower()][0]

    if all(public_key.lower() != key_data['key_sentry_id'] 
                for key_data in project_data['keys']):
        logger.error("The key does not exist in the project.")
        return

    keys_count = len(project_data['keys'])
    key_data = [key_data for key_data in project_data['keys'] if public_key.lower() == key_data['key_sentry_id']][0]

    if not project_data['limit']['fixed']:
        limit_value = (limit + ((keys_count - 1) * MIN_LIMIT_COUNT) if keys_count > 1 else limit)
        if not checking_available_limit(organization_data, limit_value):
            return

    if project_data['limit']['fixed'] and (keys_count - 1) > 0:
        if (round((project_data['limit']['count'] - limit) / ((keys_count - 1) if (keys_count - 1) > 0 else 1)) < MIN_LIMIT_COUNT):
            logger.error("The limit is not enough for other keys, increase the limit for the project.")
            return
        
    if project_data['limit']['fixed'] and (keys_count - 1) == 0:
        if (round((project_data['limit']['count'] - limit) / ((keys_count - 1) if (keys_count - 1) > 0 else 1)) < 0):
            logger.error("The project's available limit has been exceeded.")
            return

    if (limit == [limit_data['count'] for limit_data in objects.limits if key_data['limit_id'] == limit_data['id']][0] and key_data['limit']['fixed']):
        logger.warning("This limit has already been set.")
        return

    count = limit
    window = DEFAULT_LIMIT_WINDOW
    description = "Limit for the keys {0}. {1}".format(public_key, desc if desc else '')

    objects = Database()

    limit_id = objects.insert_one_row(Limit, 
                        count = count, 
                        window = window, 
                        description = description,
                        fixed = True
                    )
    
    if objects.update_limit(Key, 
                        id = key_data['id'], 
                        limit_id = limit_id
                    ):
        logger.info("The limit for the key [{0}] have been updated.".format(public_key))
        return

@click.group()
def update():
    """Update the data in the database."""

@update.command()
@click.option(
    "-o", "--organization-name", "organization_name",
    type=str,
    required=False,
    expose_value=True,
    help="Organization name. Not display name."
)
@click.option(
    "-p", "--project-name", "project_name",
    type=str,
    required=False,
    expose_value=True,
    help="Project name."
)
@click.option(
    "-k", "--public-key", "public_key",
    type=str,
    required=False,
    expose_value=True,
    help="Public key."
)
@click.option(
    "-l", "--limit-count", "limit",
    type=int,
    required=True,
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
def limit(organization_name, project_name, public_key, limit, desc):
    """Update limit.

    Examples:

    \b
        $ sentry-rate-limit update limit --organization-name test --limit-count 500 --desc "Testing."
        $ sentry-rate-limit update limit --organization-name test --project-name LoadTest --limit-count 100
        $ sentry-rate-limit update limit --organization-name test --project-name LoadTest --public-key cec9dfceb0b74c1c9a5e3c135585f364 --limit-count 50
    """

    logger.info("Starting update limit.")

    if public_key:
        if project_name:
            if organization_name:
                key(
                    public_key = public_key,
                    project_name = project_name,
                    organization_name = organization_name,
                    limit = limit,
                    desc = desc,
                )
                logger.info("Stopping update limit.")
                return
            else:
                logger.error("The organization is not specified.")
                logger.info("Stopping update limit.")
                return
        else:
            logger.error("The project is not specified.")
            logger.info("Stopping update limit.")
            return
    
    if project_name:
        if organization_name:
            project(
                project_name = project_name, 
                organization_name = organization_name,
                limit = limit,
                desc = desc,
            )
            logger.info("Stopping update limit.")
            return
        else:
            logger.error("The organization is not specified.")
            logger.info("Stopping update limit.")
            return

    if organization_name:
        organization(
            organization_name = organization_name, 
            limit = limit,
            desc = desc,
        )
        logger.info("Stopping update limit.")
        return
    else:
        logger.error("There is not a single value to update.")
        logger.info("Stopping update limit.")
        return

