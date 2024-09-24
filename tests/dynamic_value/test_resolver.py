import pytest
from nominatim_data_analyser.core.dynamic_value import Variable
from nominatim_data_analyser.core.dynamic_value.resolver import (_contains_dynamic_value,
                                                  _is_dynamic_value,
                                                  _resolve_if_resolvable,
                                                  is_resolvable, resolve_all,
                                                  resolve_one)

def test_resolve_all() -> None:
    """
        Test the resolve_all() function. Nested
        DynamicValue is tested here.
    """
    variable1 = Variable('var_name1')
    variable2 = Variable('var_name2')
    variable3 = Variable('var_name3')
    data = {
        'var_name1': variable2,
        'var_name2': variable3,
        'var_name3': 'var_value3',
    }
    assert resolve_all(variable1, data) == 'var_value3'

def test_resolve_one(variable: Variable) -> None:
    """
        Test the resolve_one() function with different
        possible data types. If any Variable is contained inside
        the data it gets resolved.
    """
    data = {'var_name': 'var_value'}
    to_resolve = [
        variable,
        [20, variable, 20, variable],
        (20, variable),
        {variable: 20, 'key': variable},
        [20, 20],
        (20, 20),
        {20:20, 'key': 'value'},
        20
    ]
    expected = [
        'var_value',
        [20, 'var_value', 20, 'var_value'],
        (20, 'var_value'),
        {'var_value': 20, 'key': 'var_value'},
        [20, 20],
        (20, 20),
        {20:20, 'key': 'value'},
        20
    ]
    for i in range(len(to_resolve)):
        assert resolve_one(to_resolve[i], data) == expected[i]

def test_is_resolvable(variable: Variable) -> None:
    """
        Test the _is_resolvable() function with different
        possible data types. If any Variable is contained inside
        the data, True should be returned.
    """
    assert is_resolvable(variable) == True
    assert is_resolvable([20, variable, 20]) == True
    assert is_resolvable((20, variable, 20)) == True
    assert is_resolvable({variable: 20, 'key': 'value'}) == True
    assert is_resolvable({20: variable, 'key': 'value'}) == True
    assert is_resolvable({20: 20, 'key': 'value'}) == False
    assert is_resolvable((20, 20, 20)) == False
    assert is_resolvable([20, 20, 20]) == False
    assert is_resolvable(20) == False

def test_contains_dynamic_value(variable: Variable) -> None:
    """
        Test the _contains_dynamic_value() function with one
        array containing a dynamic value and another that does not.
    """
    assert _contains_dynamic_value([20, variable, 20]) == True
    assert _contains_dynamic_value([20, 20, 20]) == False

def test_is_dynamic_value(variable: Variable) -> None:
    """
        Test the _is_dynamic_value() function with a
        dynamic value and with a classic value.
    """
    assert _is_dynamic_value(variable) == True
    assert _is_dynamic_value(20) == False

def test_resolve_if_resolvable(variable: Variable) -> None:
    """
        Test the _resolve_if_resolvable() function with a
        resolvable and an unresolvable data.
    """
    data = {'var_name': 'value'}
    assert _resolve_if_resolvable(data, variable) == 'value'
    assert _resolve_if_resolvable(data, 20) == 20

@pytest.fixture
def variable() -> Variable:
    return Variable('var_name')
