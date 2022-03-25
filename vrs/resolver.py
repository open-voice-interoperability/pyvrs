import base64
import dns.resolver
import json
import logging
import requests
import shlex
from vrs import is_base64, is_json

logger = logging.getLogger('pyvrs')


class VRSDecodeError(Exception):
    """Catchall VRS error for decoding issues."""


class Resolver:
    """Base resolver class."""


class RESTResolver(Resolver):

    def __init__(self, conf):
        self.conf = conf

    def login(self, uri):
        # TODO: some sort of credential management needed here
        pass

    def resolve(self, name):
        """Resolve keywords against known ReST APIs."""
        for uri in self.conf["restapi"]:
            try:
                logger.debug(f'querying: {uri}')
                self.login(uri)
                response = requests.post(uri, dict(name=name))
                logger.debug(f'response: {response}')
                response.raise_for_status()
                yield response.txt
            except Exception as e:
                logger.warn(f"{e}")
                yield


class DNSResolver(Resolver):

    def __init__(self, conf):
        self.conf = conf

    def resolve(self, name):
        """Resolve any TXT records in <subdomain>.<domain>"""
        for base in self.conf['hostname']:
            try:
                answers = dns.resolver.resolve(f'{name}.{base}', 'TXT')
                logger.debug(f'querying: {answers.qname}')
                for a in answers:
                    yield self.decode(a)
            except Exception:
                yield

    def decode(self, rdata):
        logger.debug(f"rdata: '{rdata}'")
        try:
            txt = (rdata.to_text().encode('raw_unicode_escape')
                   .decode('unicode_escape').strip("'\""))
            logger.debug(f"txt: '{txt}'")
            if is_base64(txt):
                return str(base64.b64decode(txt), 'utf8').strip()
            elif is_json(txt):
                return json.loads(txt)
            elif all([r in txt for r in ('dest', 'name', 'country')]):
                # this is in plaintext, not encoded
                d = {}
                for i in shlex.split(txt):
                    d.update([i.split("=")])
                return d
            else:
                return rdata.strings
        except Exception as ex:
            raise VRSDecodeError(ex)


def resolve(name, conf):
    """Resolve the name via the known resolver classes."""
    for klass in RESTResolver, DNSResolver:
        for record in klass(conf).resolve(name):
            yield record
