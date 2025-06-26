import os


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
