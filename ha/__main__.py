import click
import importlib
import pkgutil
from ha.pluginloader import PluginLoader
from colorama import Fore, Back, Style, init as colorama_init

colorama_init(autoreset=True)

@click.group()
def cli():
    pass

@cli.group(invoke_without_command=True)
@click.pass_context
def remote(ctx):
    if ctx.invoked_subcommand is None:
        click.secho("Available remote plugins:")
        for name in remote.list_commands(ctx):
            cmd = remote.get_command(ctx, name)
            doc = cmd.help or "no description"
            click.secho(f"{Fore.LIGHTCYAN_EX}{name}\n\t{Fore.WHITE}{doc}")

@cli.group(invoke_without_command=True)
@click.pass_context
def shellgen(ctx):
    if ctx.invoked_subcommand is None:
        click.secho("Available shellgen plugins:")
        for name in shellgen.list_commands(ctx):
            cmd = shellgen.get_command(ctx, name)
            doc = cmd.help or "no description"
            click.secho(f"{Fore.LIGHTCYAN_EX}{name}\n\t{Fore.WHITE}{doc}")

@cli.group(invoke_without_command=True)
@click.pass_context
def serve(ctx):
    if ctx.invoked_subcommand is None:
        click.secho("Available serve plugins:")
        for name in serve.list_commands(ctx):
            cmd = serve.get_command(ctx, name)
            doc = cmd.help or "no description"
            click.secho(f"{Fore.LIGHTCYAN_EX}{name}\n\t{Fore.WHITE}{doc}")

_remote_plugin_dir = "plugins/remote"
_remote_plugin_loader = PluginLoader(_remote_plugin_dir)
for plugin in _remote_plugin_loader.load():
    remote.add_command(plugin)
if len(_remote_plugin_loader.plugins) == 0:
    click.secho("No remote plugins found!", fg="red")

_shellgen_plugin_dir = "plugins/shellgen"
_shellgen_plugin_loader = PluginLoader(_shellgen_plugin_dir)

for plugin in _shellgen_plugin_loader.load():
    shellgen.add_command(plugin)

if len(_shellgen_plugin_loader.plugins) == 0:
    click.secho("No shellgen plugins found!", fg="red")

_serve_plugin_dir = "plugins/serve"
_serve_plugin_loader = PluginLoader(_serve_plugin_dir)

for plugin in _serve_plugin_loader.load():
    serve.add_command(plugin)

if len(_serve_plugin_loader.plugins) == 0:
    click.secho("No serve plugins found!", fg="red")