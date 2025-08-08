###
# #%L
# aiSSEMBLE::Universal Config::Loader
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from .properties_exporter_base import PropertyExporterBase

CONFIG_DIR = "/configurations/base/"


class PropertyExporter(PropertyExporterBase):
    """aiSSEMBLE-universal-config properties exporter class."""

    def __init__(self, caller_locals, caller_globals):
        self.globals = caller_globals
        self.locals = caller_locals

    def extract_vars_to_property_file(
        self,
        file_name="configuration.properties",
        relative_file_path="../configurations/base/",
    ):
        local_properties = self._get_properties_from_context(self.locals)
        global_properties = self._get_properties_from_context(self.globals)

        combined_properties = list(set(local_properties + global_properties))

        self.save_properties_to_config_directory(
            file_name, relative_file_path, combined_properties
        )

    def _get_properties_from_context(self, context):
        # Show only user-defined variables (excluding built-ins)
        user_defined_vars = self._get_user_defined_vars_from_context(context)
        string_and_int_var_names = self._filter_string_and_int_vars(user_defined_vars)
        var_values = [user_defined_vars[n] for n in string_and_int_var_names]

        properties = []
        for key, value in zip(string_and_int_var_names, var_values):
            properties.append(f"{key}={value}")

        return properties

    def _get_user_defined_vars_from_context(self, context):
        user_defined_vars = {k: v for k, v in context.items() if not k.startswith("_")}
        return user_defined_vars

    def _filter_string_and_int_vars(self, public_vars):
        typeset = set(["str", "int"])
        var_names = [i for i in public_vars if type(public_vars[i]).__name__ in typeset]

        return var_names
