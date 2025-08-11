###
# #%L
# aiSSEMBLE::Universal Config::Loader
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import os
from ..util.utils import print_next_step, TITLE_DIVIDER
from abc import ABC, abstractmethod

CONFIG_DIR = "/configurations/base/"


class PropertyExporterBase(ABC):
    """aiSSEMBLE-universal-config config helper base class."""

    @abstractmethod
    def extract_vars_to_property_file(
        self,
        file_name="configuration.properties",
        relative_file_path="../configurations/base/",
    ):
        """
        Extract vars (str type and int type only) into a .properties file. File will be generated if it doesn't exist.
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
        pass

    def save_properties_to_config_directory(
        self, file_name, relative_file_path, properties
    ):
        os.environ["KRAUSENING_BASE"] = os.path.abspath(relative_file_path)
        try:
            # create config directory if not exists
            os.makedirs(relative_file_path, exist_ok=True)

            file_name = f"{relative_file_path}{file_name}"

            self._write_to(file_name=file_name, content=properties)

        except FileExistsError as fe:
            print(
                f"Error creating the configuration directory at {relative_file_path}. {fe}"
            )
        except OSError as e:
            print(
                f"Error creating the configuration directory, you can set the relative_file_path for the configuration file. {e}"
            )

    def _read_from(self, file_name: str) -> []:
        # Read the file content line by line into a list
        file_lines = []
        with open(file_name, "r") as file:
            file_lines = file.readlines()

        return file_lines

    def _write_to(self, file_name: str, content: []):
        try:
            file_name = os.path.expanduser(file_name)
            file_exists = os.path.isfile(file_name)
            final_content = []
            mode = "w"
            if not file_exists:
                final_content = content
            else:
                file_lines = self._read_from(file_name)
                mode = "a"
                for line in content:
                    if (line.strip() + "\n") not in file_lines:
                        final_content.append(line)

            with open(file_name, mode) as f:
                for line in final_content:
                    f.write(line + "\n")

            print_next_step(
                f"{self._load_property_instruction(config_path=os.getenv('KRAUSENING_BASE'))}",
                f"Optional{TITLE_DIVIDER}The variables have been extracted to {os.path.abspath(file_name)}.\n You can remove the following variables from your notebook and load them via the ConfigLoader:\n {final_content}",
            )
        except Exception as e:
            print(f"Failed to write to configuration file: {e}")

    def _load_property_instruction(self, config_path: str) -> str:
        return (
            f"Required{TITLE_DIVIDER}To load property values as global variables, add the below code snippets to a new cell and run the cell:"
            + "\n\n```"
            + "\n# import the ConfigLoader module"
            + "\nfrom aissemble_universal_config_loader.config_loader import ConfigLoader"
            + "\n"
            + "\n# set configuration file directory, this is for bootstrapping the library"
            + f"\nos.environ['KRAUSENING_BASE'] = '{config_path}'"
            + "\n"
            + "\n# load property values as global variables"
            + "\nConfigLoader().load_as_global()"
            + "\n\n```"
            + "\n Note: Use `ConfigLoader().load_as_env()` to load property values as environment variable."
            + "\n"
        )


class PropertyExportHelper(PropertyExporterBase):
    def extract_vars_to_property_file(
        self,
        file_name="configuration.properties",
        relative_file_path="../configurations/base/",
    ):
        pass
