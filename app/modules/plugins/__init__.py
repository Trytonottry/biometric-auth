import importlib
import os

PLUGINS_DIR = os.path.join(os.path.dirname(__file__))

def load_plugins():
    plugins = {}
    for fname in os.listdir(PLUGINS_DIR):
        if fname.endswith('.py') and fname != '__init__.py':
            module_name = f"app.modules.plugins.{fname[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'authenticate'):
                plugins[fname[:-3]] = module.authenticate
    return plugins