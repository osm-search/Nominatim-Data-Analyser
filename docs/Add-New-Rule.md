# Add a basic rule
To add a new rule, a YAML Rule file should be created inside the `analyser/rules_specifications` folder. The YAML file name should be unique and it will be equal to the name of the rule (as much as possible).

The content of the file should follows the [YAML Rule Specification](YAML-Rule-Specification.md) format.

# Create custom pipes (python code)

If a more advanced rule needs a custom python logic, a custom `Pipe` can be created.
To do that, a folder with the name of the rule should be created inside the `analyser/core/pipes/rules_specific_pipes` folder. 

A python file should be created inside the newly created folder. This file should contain a class which inherits from the `Pipe` base class. See the [Pipe base class](Pipes.md#The-Pipe-base-class) chapter to understand how the base `Pipe` class works and how to create a custom pipe from it.

The custom `Pipe` class should be imported inside the `__init__.py` of the `analyser/core/pipes/rules_specific_pipes` so that it can be found by the `Assembler` (See [Architecture](Overview.md#architecture)).

Once the custom pipe well created, it can be used in the [YAML Rule Specification](YAML-Rule-Specification.md) by setting its `class` name as the value of the `type` field.