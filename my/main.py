import importlib
import os
import json
from collections import OrderedDict


def import_from_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    # sentence_transformers.models.Transformer
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        raise ImportError(msg)

    try:
        module = importlib.import_module(dotted_path)
    except:
        module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)
        raise ImportError(msg)

model_path = "../models/roberta"

modules_json_path = os.path.join(model_path, 'modules.json')
with open(modules_json_path) as fIn:
    modules_config = json.load(fIn)

modules = OrderedDict()
for module_config in modules_config:
    module_class = import_from_string(module_config['type'])
    module = module_class.load(os.path.join(model_path, module_config['path']))
    modules[module_config['name']] = module