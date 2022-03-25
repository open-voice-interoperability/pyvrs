import click
import click_config_file
import click_log
import logging
import os
from pprint import pprint
from vrs.resolver import resolve


"""
Command-line entry points for the PyVRS package.
"""

logger = logging.getLogger('pyvrs')
click_log.basic_config(logger)


# see https://jwodder.github.io/kbits/posts/click-config/
@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-c', '--config', type=click.Path(dir_okay=False),
              default=f"{os.environ['HOME']}/pyvrs/pyvrs.conf")
@click.argument('name')
def vresolve(name, config):
    """Resolve <name>"""
    for record in resolve(name, config):
        pprint(record)
