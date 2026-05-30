import importlib
import pkgutil

import click


class PluginLoader(object):
    """
        Loads plugins that are click commands
    """
    def __init__(self, plugin_location: str):
        self.plugin_location = plugin_location
        self.plugins = []

    def load(self):
        for finder, name, _ in pkgutil.iter_modules([self.plugin_location]):
            package_dir = '.'.join(self.plugin_location.split("/"))
            package_name = f"{package_dir}.{name}"
            module = importlib.import_module(package_name)
            self.plugins.append(name)
            for attr in vars(module).values():
                if isinstance(attr, click.Command):
                    attr.name = name
                    self.plugins.append(name)
                    yield attr
