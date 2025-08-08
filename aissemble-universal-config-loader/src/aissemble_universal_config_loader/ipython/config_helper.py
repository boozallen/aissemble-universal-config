###
# #%L
# aiSSEMBLE::Universal Config::Loader
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
)
from ..exporter.properties_exporter_base import PropertyExportHelper

CONFIG_DIR = "/configurations/base/"


@magics_class
class ConfigHelper(Magics):
    """aiSSEMBLE-universal-config config helper class."""

    @line_magic
    def extract_vars_to_property_file(self, parameter_s):
        """
        Extract vars (str type and int type only) into a .properties file. File will be generated if not exists
        If there are no arguments are given, by default, it will be set as the configuration.properties if it's not set and
        the relative path for the property file from `current` directory. By default, it will be set to `../configurations/base` directory
                                    ├── current/
                                    │     └── foo.ipnb
                                    ├── configurations
                                    │     └── base
                                    │       └── configuration.properties
                                    └── ...
                                    Note: `UsageError` will be raised if there is no parent directory for the `current` directory

        If arguments are given, the variables will be writen to the given file within the given directory.

        Examples
        --------
        Define file name and relative file path with extract_vars_to_property_file:

          %extract_vars_to_property_file my-custom.properties

          %extract_vars_to_property_file my-custom.properties ../my/custom/folder

        """
        arg_list = parameter_s.split()
        if arg_list:
            if len(arg_list) >= 2:
                file_name = arg_list[0]
                relative_file_path = arg_list[1]
            elif len(arg_list) == 1:
                file_name = arg_list[0]
        else:
            file_name = "configuration.properties"
            relative_file_path = f"..{CONFIG_DIR}"

        user_ns = self.shell.user_ns
        property_names = self._get_property_names_filtered_by_int_and_str(user_ns)

        if not property_names:
            print("No variables match the `str` or the `int` type.")
            return

        properties = self._get_property_keys_and_values(property_names, user_ns)

        property_export_helper = PropertyExportHelper()

        property_export_helper.save_properties_to_config_directory(
            file_name, relative_file_path, properties
        )

    def _get_property_keys_and_values(self, property_names, user_ns):
        varlist = [user_ns[n] for n in property_names]
        properties = []
        for vname, var in zip(property_names, varlist):
            properties.append(f"{vname}={var}")
        return properties

    def _get_property_names_filtered_by_int_and_str(self, user_ns):
        user_ns_hidden = self.shell.user_ns_hidden
        nonmatching = object()  # This can never be in user_ns
        varnames = [
            i
            for i in user_ns
            if not i.startswith("_")
            and (user_ns[i] is not user_ns_hidden.get(i, nonmatching))
        ]
        # only read the str or int variables
        typeset = set(["str", "int"])
        varnames = [i for i in varnames if type(user_ns[i]).__name__ in typeset]
        # sort the var name list
        varnames.sort()
        return varnames


# In order to actually use these magics, you must register them with a
# running IPython.
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(ConfigHelper)
