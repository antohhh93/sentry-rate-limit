import click
from prettytable import PrettyTable

import ratelimit
from ratelimit.log import Log
from ratelimit.config import (
    LOGGING_LEVEL,
    LOGGING_ENABLE,
    LOGGING_FILE_NAME,
)

from .imports import import_string

version_string = ratelimit.__version__

if LOGGING_ENABLE:
    objects = Log(
        logging_file_name = LOGGING_FILE_NAME,
        logging_level = LOGGING_LEVEL
    )
    objects.logger_format()
    objects.logger_file_handler()
    objects.logger_stream_handler()
    objects.logger()

def print_tables_in_ASCII_format(table):
    if table:
        pt = PrettyTable()
        for obj in table:
            pt.field_names = [key for key, value in obj.items()]
            pt.add_row([value for key, value in obj.items()])
        pt.align = "l"
        pt.sortby = "id" if all("id" in obj for obj in table) else None
        return click.echo(pt)

@click.group(context_settings = {"max_content_width": 150})
@click.version_option(version = version_string)
@click.pass_context
def cli(ctx):
    """
    Sentry Rate Limit this is a utility for setting limits in.
    """

for cmd in map(
    import_string,
    (
        "ratelimit.cli.commands.add.add",
        "ratelimit.cli.commands.cleanup.cleanup",
        "ratelimit.cli.commands.delete.delete",
        "ratelimit.cli.commands.describe.describe",
        "ratelimit.cli.commands.get.get",
        "ratelimit.cli.commands.help.help",
        "ratelimit.cli.commands.init.init",
        "ratelimit.cli.commands.set.set",
        "ratelimit.cli.commands.sync.sync",
        "ratelimit.cli.commands.update.update",
    ),
):
    cli.add_command(cmd)

def main():
    func = cli
    kwargs = {
        "obj": {},
        "max_content_width": 100,
    }
    func(**kwargs)