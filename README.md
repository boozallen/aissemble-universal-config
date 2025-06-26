# aiSSEMBLE Universal Config Loader
aiSSEMBLE Universal Config Loader uses Krausening to provide features to read the configuration from property file and
load the configuration to environment variables or to global variables. For the notebook user, it also providers a
helper class to extract their notebooks global variables into the property file to set up the configuration for the
first time.

## Getting Started

### Loading Configurations

The loader uses [Krausening](https://github.com/TechnologyBrewery/krausening/tree/dev/krausening#krausening-in-one-pint-learn-krausening-in-2-minutes)
to read configurations from a properties file into either [global variables](https://docs.python.org/3/faq/programming.html#what-are-the-rules-for-local-and-global-variables-in-python)
or [environment variables](https://docs.python.org/3/library/os.html#os.environ). Krausening is useful for defining
different configurations per execution environment. For simple local usage, you can simply set `KRAUSENING_BASE` to the
directory that contains your configuration file(s). The default Krausening base location is `configurations/base` and
the default properties file is `configuration.properties`. 

```python
from aissemble_universal_config_loader.config_loader import ConfigLoader

# Tell Krausening where the configuration files are
os.environ['KRAUSENING_BASE']="configurations/base"

# Load everything in configuration.properties into global variables
ConfigLoader().load_as_global()

# Load everything in my-custom.properties into the `os.environ` map
ConfigLoader().load_as_env(file="my-custom.properties")
```

### Extracting Configurations from a Notebook

To help move projects from Jupyter Notebook experimentation to the next stage of development, Universal Configuration
can extract configurations from a Notebook cell into a configuration properties file.  The extraction function exports
all `str` or `int` constants in a cell.

```python
# constants used for configuration
MODEL_BUCKET="s3a://ml-project/models"
BATCH_SIZE=100
INPUT_LIST=[1, 2, 3]  # the list variable will not be extracted to property file
METADATA={"a":"b", "c":"d"} # the dict variable will not be extract to property file


# install the aissemble-universal-config-loader module 
!pip install aissemble-universal-config-loader
%load_ext aissemble_universal_config_loader.ipython.config_helper

# extract the `int`/`string` type global variables to the default configuration file
%extract_vars_to_property_file

# extact to a custom file/location
%extract_vars_to_property_file my-custom.properties ../my/custom/folder
```

##### Output
The extraction function will add the extracted configurations to the specified properties file, or create a new file if
it doesn't already exist.  It will also output next steps for consuming the configuration file within the Notebook or a
separate Python project.

```properties
MODEL_BUCKET="s3a://ml-project/models"
BATCH_SIZE=100
```