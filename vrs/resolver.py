import base64
import dns.resolver
import json
import logging
import requests
import shlex
from vrs import is_base64, is_json
from configparser import ConfigParser

logger = logging.getLogger('pyvrs')


class VRSDecodeError(Exception):
    """Catchall VRS error for decoding issues."""


class Resolver:
    """Base resolver class."""


class RESTResolver(Resolver):

    def __init__(self, conf):
        self.conf = conf
        self.url = self.conf['url']
        self.email = self.conf['email']
        self.password = self.conf['password']
        self.session = requests.Session()

    def login(self):
        login_url = f"{self.url}/api/login"
        login_data = {'email': self.email, 'password': self.password}
        logger.debug(f'{login_url} {login_data}')
        response = self.session.post(login_url, json=login_data)
        response.raise_for_status()

    def resolve(self, name):
        """Resolve keywords against known ReST APIs."""
        try:
            self.login()
            records_url = f"{self.url}/api/records/{name}"
            logger.debug(f'querying: {records_url}')
            response = self.session.get(records_url)
            logger.debug(f'response: {response}')
            response.raise_for_status()
            yield response.text
        except Exception as e:
            logger.warn(f"{e}")
            yield


class DNSResolver(Resolver):

    def __init__(self, conf):
        self.conf = conf

    def resolve(self, name):
        """Resolve any TXT records in <subdomain>.<domain>"""
        try:
            concat = name + "." + self.conf["hostname"]
            answers = dns.resolver.resolve(concat, 'TXT')
            logger.debug(f'querying: {answers.qname}')
            for a in answers:
                yield self.decode(a)
        except Exception as e:
            logger.warn(e)
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


def GetResolver(conf):
    if 'password' in conf:
        return RESTResolver(conf)
    elif 'hostname' in conf:
        return DNSResolver(conf)
    else:
        raise Exception(f"Invalid config block: {conf}")


def resolve(name, conf):
    """Resolve the name via each resolver config block."""

    cp = ConfigParser()
    cp.read(conf)

    for section in cp.sections():
        resolver = GetResolver(cp[section])
        logger.debug(f"resolving with section [{section}] ==> {resolver}")
        for record in resolver.resolve(name):
            yield record
