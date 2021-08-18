import pytest
from analyser.core.pipes.rules_specific_pipes import \
    AddrHouseNumberNoDigitFilter
from analyser.core.qa_rule import ExecutionContext


def test_process_addr_HN_no_digit_filter(digits_filter: AddrHouseNumberNoDigitFilter) -> None:
    """
        Test the process() method of the custom pipe AddrHouseNumberNoDigitFilter.
        Data where housenumber doesnt contain any number inside should be returned, otherwise
        the method should returns None.
    """
    data_with_numbers = {'housenumber': '15aa2', 'dumbfield': 'dumbvalue'}
    data_without_numbers = {'housenumber': 'aa', 'dumbfield': 'dumbvalue'}

    assert digits_filter.process(data_with_numbers) == None
    assert digits_filter.process(data_without_numbers) == data_without_numbers

@pytest.fixture
def digits_filter(execution_context: ExecutionContext) -> AddrHouseNumberNoDigitFilter:
    return AddrHouseNumberNoDigitFilter({}, execution_context)
