import click

#TODO в разработке

@click.group()
def describe():
    """DESCRIBE."""

@describe.group()
@click.option(
    "-o", "--organization-name", "organization",
    type=str,
    required=False,
    expose_value=True,
    help="Organization name. Not display name."
)
@click.option(
    "-p", "--project-name", "project",
    type=str,
    required=False,
    expose_value=True,
    help="Project name."
)
@click.option(
    "-k", "--public-key", "key",
    type=str,
    required=False,
    expose_value=True,
    help="Public key."
)

def limit():
    """LIMIT."""

@limit.command()
@click.argument(
    "name", 
    required=True
)
def organization(name):
    """
    По организации
    """

@limit.command()
@click.argument(
    "name", 
    required=True
)
def project(name):
    """
    По проекту
    """

@limit.command()
@click.argument(
    "name", 
    required=True
)
def key(name):
    """
    По ключу
    """