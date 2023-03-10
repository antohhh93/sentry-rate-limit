import click
import logging

from ratelimit.db import (
    Database,
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

"""
cleanup.cleanup_limit:
    проверяет фиксированные лимиты на использование в базе данных
    удаляет неиспользуемые фиксированные лимиты из базы данных

cleanup.cleanup_project:
    проверет зависимости между проектами и организациями в базе данныз
    удаляет проекты без зависимостей из базы данных

cleanup.cleanup_key:
    проверет зависимости между ключами и проектами в базе данныз
    удаляет проекты без зависимостей из базы данных
"""

logger = logging.getLogger()

def cleanup_limit():
    objects = LimitDatabase()
    objects.get_limit()

    limit_delete: list = []

    for limit_data in objects.limits:
        if limit_data['fixed']:
            if all(limit_data['id'] != organization_data['limit_id'] for organization_data in OrganizationDatabase().get_organizations()):
                if all(limit_data['id'] != organization_data['limit_id'] for organization_data in ProjectDatabase().get_projects()):
                    if all(limit_data['id'] != organization_data['limit_id'] for organization_data in KeyDatabase().get_keys()):
                        limit_delete.append(limit_data)

    if not limit_delete:
        logger.warning("Cleaning of limits is not required.")
        return

    delete(limit_delete, Limit)

def cleanup_project():
    objects = ProjectDatabase()
    objects.get_projects()

    project_delete: list = []

    for project_data in objects.projects:
        if all(project_data['id'] != organization_data['project_id'] for organization_data in OrganizationProjectDatabase().get_organization_projects()):
            project_delete.append(project_data)

    if not project_delete:
        logger.warning("Cleaning of projects is not required.")
        return

    delete(project_delete, Project)

def cleanup_key():
    objects = KeyDatabase()
    objects.get_keys()

    key_delete: list = []

    for key_data in objects.keys:
        if all(key_data['id'] != project_data['key_id'] for project_data in ProjectKeyDatabase().get_project_key()):
            key_delete.append(key_data)

    if not key_delete:
        logger.warning("Cleaning of keys is not required.")
        return

    delete(key_delete, Key)

def delete(data_dict, model):
    objects = Database()

    for data in data_dict:
        if objects.recursive_delete_id(model, data['id']):
            logger.info("{0} removed from database.".format(model.__name__))

@click.command()
def cleanup():
    """Delete data without dependencies."""

    logger.info("Starting cleanup.")

    cleanup_limit()
    cleanup_project()
    cleanup_key()

    logger.info("Stopping cleanup.")