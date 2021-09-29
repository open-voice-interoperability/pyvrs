import click
import click_log
import logging
from pprint import pprint
import vrs

"""
Command-line entry points for the PyVRS package.
"""

logger = logging.getLogger('pyvrs')
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-r', '--resolver', default='ovon.directory')
@click.argument('name')
def vresolve(resolver, name):
    """Resolve <name>"""
    logger.info(f"resolver='{resolver}' name='{name}'")
    answers = vrs.resolve(name, resolver)
    for rr in answers:
        pprint(rr)
