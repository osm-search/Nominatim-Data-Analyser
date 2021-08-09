
from analyser.core.dynamic_value import Variable
import pytest

def test_resolve_variable_ok(variable: Variable) -> None:
    """
        Test the resolve() method of the Variable class without
        raising any exception.
    """
    data = {
        'test_key1': 'test_val1',
        'var_name': 'test_val2',
        'test_key2': 'test_val3'
    }
    assert variable.resolve(data) == 'test_val2'

def test_resolve_variable_dont_exist(variable: Variable) -> None:
    """
        Test the resolve() method of the Variable class by
        giving data without the var_name inside.
    """
    data = {
        'test_key1': 'test_val1',
        'test_key2': 'test_val2',
        'test_key3': 'test_val3'
    }
    with pytest.raises(Exception, match='The variable name var_name was not found in the input dictionnary.'):
        variable.resolve(data)

@pytest.fixture
def variable() -> Variable:
    return Variable('var_name')

