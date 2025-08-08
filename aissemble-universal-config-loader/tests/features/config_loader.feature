Feature: Test ConfigLoader Implementation

  Scenario Outline: The universal configuration loader loads all property into environment and global variables
    Given A property file
    When universal configuration loader loads the property with "<destination_flag>" set
    Then the properties can be accessed

    Examples:
      | destination_flag |
      | to_env           |
      | to_var           |
      | none             |


  Scenario Outline: The universal configuration loader saves user defined variables in a properties file
    Given properties exist in a python session
    When universal configuration loader extracts the properties using native python
    Then the properties are saved to a properties file
