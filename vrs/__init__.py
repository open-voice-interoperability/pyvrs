import base64
import json
import logging

logger = logging.getLogger('pyvrs')


class VRSDecodeError(Exception):
    pass


def is_base64(s):
    """Return True if input string is base64, false otherwise."""
    s = s.strip("'\"")
    try:
        if isinstance(s, str):
            sb_bytes = bytes(s, 'ascii')
        elif isinstance(s, bytes):
            sb_bytes = s
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
