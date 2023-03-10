import click
from ratelimit.cli import print_tables_in_ASCII_format as print_table

#TODO в разработке

def organization(name):
    """
    По организации
    """

def project(name):
    """
    По проекту
    """

def key(name):
    """
    По ключу
    """

@click.group()
def get():
    """GET."""

@get.command()
@click.option(
    "-O", "--organization", "organization_name",
    is_flag=True,
    expose_value=True,
    help="For all organizations."
)
@click.option(
    "-P", "--project", "project_name",
    is_flag=True,
    expose_value=True,
    help="For all projects."
)
@click.option(
    "-k", "--public-key", "public_key",
    is_flag=True,
    expose_value=True,
    help="For all keys."
)
def limit(organization_name, project_name, public_key):
    """LIMIT."""

    if public_key:
        return key(
            name = public_key,
        )
    
    if project_name:
        return project(
            name = project_name,
        )

    if organization_name:
        return organization(
            name = organization_name,
        )
    else:
        return click.secho(
            "Error. There is not a single value to get.",
            err=True,
            fg="red",
        ) #TODO переделать на логгер

@get.command()
@click.option(
    "-M", "--model", "model",
    is_flag=True,
    expose_value=True,
    help="Description of the model class Organization."
)
@click.option(
    "-J", "--json", "json",
    is_flag=True,
    expose_value=True,
    help="Output in json format."
)
def organization(model, json):
    """Extracting organizations' data."""

    if model:
        from playhouse.reflection import print_model
        from ratelimit.db import Organization

        return print_model(Organization)
    
    from ratelimit.db import OrganizationDatabase

    objects = OrganizationDatabase()
    objects.get_organizations()
    
    if all(not organization 
                for organization in objects.organizations):
        return click.secho(
            "Error. No data to sync.",
            err=True,
            fg="red",
        ) #TODO переделать на логгер
    
    if json:
        from ratelimit.utils.json import output_json
        
        name: dict = {}
        name['organizations'] = objects.organizations

        return click.echo(
            output_json(name)
        )

    return print_table(objects.organizations)