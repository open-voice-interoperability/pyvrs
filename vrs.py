#!/usr/bin/env python3

import base64
import click
import dns.resolver
import json
import shlex


@click.command()
@click.option('-r', '--resolver', default='ovon.directory')
@click.argument('name')
def resolve(resolver, name):
    """Resolve <name>"""
    answers = dns.resolver.resolve('target.ovon.directory', 'TXT')
    #print(answers.qname)
    for rdata in answers:
        print(decode(rdata))


def decode(rdata):
    # TODO: decode base64-encoded data
    #import pdb; pdb.set_trace()
    #print(dir(rdata))
    #print(rdata.to_text())
    txt = rdata.to_text()
    if is_simple(txt):
        return dict(item.split("=") for item in shlex.split(shlex.split(txt)[0]))
    elif is_base64(txt):
        return base64.b64decode(txt)
    elif is_json(txt):
        return json.loads(txt) 
    else:
        return rdata.strings


def is_simple(s):
    required = ['dest', 'name', 'country']
    return all([r in s for r in required])


def is_base64(sb):
    """Return True if input string is base64, false otherwise."""
    try:
        if isinstance(sb, str):
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def is_json(s):
    try:
        json.loads(s)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    resolve()
