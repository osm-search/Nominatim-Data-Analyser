from nominatim_data_analyser.core.dynamic_value.switch import Switch
import pytest

def test_resolve_switch_ok(switch: Switch) -> None:
    """
        Test the resolve() method of the Switch class without
        raising any exception.
    """
    data = {
        'test_key1': 'test_val1',
        'test_expression': 'case2',
        'test_key2': 'test_val3'
    }
    assert switch.resolve(data) == 'result2'

def test_resolve_switch_expression_dont_exist(switch: Switch) -> None:
    """
        Test the resolve() method of the Switch class by using a data
        dictionnary which doesn't contain the switch expression in its keys.
    """
    data = {
        'test_key1': 'test_val1',
        'test_key2': 'case2',
        'test_key2': 'test_val3'
    }
    with pytest.raises(Exception, match='The expression test_expression was not found in the input dictionnary.'):
        switch.resolve(data)

def test_resolve_switch_case_dont_exist(switch: Switch) -> None:
    """
        Test the resolve() method of the Switch class by using a
        case which isn't configured in the switch.
    """
    data = {
        'test_key1': 'test_val1',
        'test_expression': 'wrong_case',
        'test_key2': 'test_val3'
    }
    with pytest.raises(Exception, match=r'The case wrong_case is not in the configured switch cases.*'):
        switch.resolve(data)

@pytest.fixture
def switch() -> Switch:
    return Switch('test_expression', {
        'case1': 'result1',
        'case2': 'result2',
        'case3': 'result3'
    })
