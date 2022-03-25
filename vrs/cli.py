import click
import click_config_file
import click_log
import logging
from pprint import pprint
from vrs.resolver import resolve


"""
Command-line entry points for the PyVRS package.
"""

logger = logging.getLogger('pyvrs')
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-H', '--hostname', default=['ovon.directory'], multiple=True)
@click.option('-r', '--restapi', multiple=True)
@click.argument('name')
@click_config_file.configuration_option()
def vresolve(name, hostname, restapi):
    """Resolve <name>"""
    logger.debug(f"{hostname} / {restapi} / {name}")

    # coax the config parameters into arrays
    # TODO: turn this into a full-fledged config object
    if isinstance(hostname, str):
        hostname = [hostname]
    if isinstance(restapi, str):
        restapi = [restapi]

    for record in resolve(name, dict(hostname=hostname, restapi=restapi)):
        pprint(record)
