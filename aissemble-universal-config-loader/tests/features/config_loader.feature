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
