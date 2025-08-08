import os
import sys
import shutil

folder_path = os.path.join(os.path.dirname(__file__), "steps")
folder_path = os.path.abspath(folder_path)
sys.path.append(folder_path)
from config_loader_steps import RELATIVE_FILE_PATH


def before_all(context):
    os.environ["KRAUSENING_BASE"] = "tests/resources/configurations"


def after_scenario(context, scenario):
    for x in ["key1", "key2", "key-3", "key_4"]:
        # clean up environment variables
        if os.environ.get(x, None) is not None:
            os.environ.pop(x)
        # clean up global variables
        key = x.replace("-", "_")
        if hasattr(context, "globals") and key in context.globals:
            del context.globals[key]

    if os.path.exists(RELATIVE_FILE_PATH) and os.path.isdir(RELATIVE_FILE_PATH):
        shutil.rmtree(RELATIVE_FILE_PATH)
