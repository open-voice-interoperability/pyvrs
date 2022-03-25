# PyVRS

PyVRS is Voice Registry System ("VRS") resolver library, similar to a DNS
resolver, implemented in Python3.

For more information on VRS, see <https://github.com/open-voice-network/vrs>.

## Usage

### As a library

```python
import os
from vrs.resolver import resolve

CONF = f"{os.environ['HOME']}/.config/pyvrs/pyvrs.conf"
@click.argument('name')
for record in resolve(name, config):
    pprint(record)
```

### From the command-line

This library includes a command-line script that also understands the
VRS-specific `resolv.conf`:

```sh
% vresolve --config myvrs.conf big-tin-can
```

Run `vresolve --help` for more command line options.

## VRS resolver config file format

VRS understands two different types data sources: one DNS-based and one
using a ReST API. Just like regular DNS, the resolver can try more than
one server.

```ini
# hostnames with TXT records defining VRS data
[dns1]
hostname = ovon.directory

# there can be more than one of each type
[dns1]
hostname = voice-agents.directory

# IP addresses / hostnames of VRS ReST APIs
[local-rest]
url = http://localhost:8080/
email = me@example.com
password = secret
```
