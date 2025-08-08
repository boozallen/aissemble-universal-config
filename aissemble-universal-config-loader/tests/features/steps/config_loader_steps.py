from behave import given, then, when
from nose.tools import eq_, ok_
import os
from aissemble_universal_config_loader.config_loader import (
    ConfigLoader,
)
from aissemble_universal_config_loader.exporter.properties_exporter import (
    PropertyExporter,
)

PROPERTIES_FILE_NAME = "configuration.properties"

RELATIVE_FILE_PATH = "./target/configuration/base/"


@given("A property file")
def given_a_property_file(context):
    context.loader = ConfigLoader()
    context.file = "test.properties"
    context.globals = globals()
    context.properties = {
        "key1": "value1",
        "key2": "value2",
        "key-3": "value3",
        "key_4": "value4",
    }


@when('universal configuration loader loads the property with "{destination_flag}" set')
def when_universal_config_loader_loads_the_property_with_destination_flag_set(
    context, destination_flag
):
    context.destination_flag = destination_flag
    match destination_flag:
        case "to_env":
            context.loader.load_as_env(context.file)
        case "to_var":
            context.loader.load_as_global(context.file)
        case _:
            context.loader.load(context.file)


@then("the properties can be accessed")
def all_properties_in_the_property_file_is_loaded_correctly(context):
    for key in context.properties.keys():
        assert_property_load_correctly(
            context.destination_flag, key, context.properties.get(key)
        )


@given("properties exist in a python session")
def properties_exist_in_a_python_session(context):
    pass


@when("universal configuration loader extracts the properties using native python")
def universal_configuration_loader_extracts_the_properties_using_native_python(context):
    MODEL_BUCKET = "s3a://ml-project/models"
    BATCH_SIZE = 100
    property_exporter = PropertyExporter(locals(), globals())

    property_exporter.extract_vars_to_property_file(
        relative_file_path=RELATIVE_FILE_PATH
    )


@then("the properties are saved to a properties file")
def the_properties_are_saved_to_a_properties_file(context):
    file_name = f"{RELATIVE_FILE_PATH}{PROPERTIES_FILE_NAME}"
    with open(file_name, "r") as file:
        file_lines = file.readlines()
        file_lines = ",".join(file_lines)

        ok_("MODEL_BUCKET" in file_lines)
        ok_("BATCH_SIZE" in file_lines)


def assert_property_load_correctly(type: str, key: str, value: str):
    match type:
        case "to_env":
            eq_(os.getenv(key), value)
        case "to_var":
            eq_(globals()[key.replace("-", "_")], value)
        case _:
            eq_(os.environ.get(key.upper(), None), None)
            ok_(key.replace("-", "_") not in globals())
