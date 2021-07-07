from analyser.core.exceptions import YAMLSyntaxException
from typing import Tuple
import re

type_condition_regex = re.compile(r'/\?([nrw]{2,3})\?/')
check_value_regex = re.compile(r'-> \$(.*)')

def parse_complex_value(value: any, data: dict = None) -> any:
    """
        Parses a complex custom YAML value and extract
        the right value.

        Handles the /?nwr?/ condition and the $ custom variable
        assignment.
    """
    #Convert a dict type to a tuple (first key, value pair)
    if isinstance(value, dict):
        first_key = list(value.keys())[0]
        if type_condition_regex.match(first_key):
            value = (first_key, value[first_key])

    if isinstance(value, Tuple):
        #Detects the /?nwr?/ condition
        type_condition_match = type_condition_regex.match(value[0])
        if type_condition_match:
            #Gets the value to check (the one starting with $)
            value_to_check = check_value_regex.search(value[0]).group(1)
            types = type_condition_match.group(1)
            for i, type in enumerate(types):
                if type.lower() == data[value_to_check].lower():
                    return replace_all_custom_var(value[1][i], data)

    return replace_all_custom_var(value, data)

def replace_all_custom_var(value: any, data: dict = None) -> any:
    """
        Replaces each custom variable ($) with its
        right value.
    """
    if isinstance(value, dict):
        return {replace_one_custom_var(k, data): replace_one_custom_var(v, data) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_one_custom_var(v, data) for v in value]
    elif isinstance(value, tuple):
        return (replace_one_custom_var(value[0], data), replace_one_custom_var(value[1], data))
    else:
        return replace_one_custom_var(value, data)

def replace_one_custom_var(value: any, data: dict = None) -> any:
    """
        Replaces the value with the right value from the data
        if its a custom variable ($).
    """
    if isinstance(value, str) and value[0] == '$':
        name = value[1:]
        if not name in data:
            raise YAMLSyntaxException(f'The {name} value doesn\'t exist.')
        return data[name]
    return value


