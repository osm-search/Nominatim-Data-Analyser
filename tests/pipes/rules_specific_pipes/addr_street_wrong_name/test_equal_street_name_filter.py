import pytest

from nominatim_data_analyser.core.pipes import EqualStreetNameFilter
from nominatim_data_analyser.core.qa_rule import ExecutionContext


@pytest.fixture
def equal_street_name_filter(
        execution_context: ExecutionContext) -> EqualStreetNameFilter:
    return EqualStreetNameFilter({}, execution_context)


def test_matching_street_name_passes_through(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Rua das Flores',
        'full_name_set': {'name': 'Rua das Flores'}
    }
    result = equal_street_name_filter.process(data)
    assert result is not None


def test_ref_based_naming_not_flagged(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Rodovia BR-116',
        'full_name_set': {'ref': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is None


def test_ref_based_naming_with_name_not_flagged(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Rodovia BR-116',
        'full_name_set': {'name': 'Rodovia Santos Dumont', 'ref': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is None


def test_ref_not_matching_passes_through(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Rua das Flores',
        'full_name_set': {'ref': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is not None


def test_ref_equal_to_street_passes_through(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'BR-116',
        'full_name_set': {'ref': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is not None


def test_empty_full_name_set_passes_through(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Rodovia BR-116',
        'full_name_set': {}
    }
    result = equal_street_name_filter.process(data)
    assert result is not None


def test_prefix_plus_stem_filtered(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Rodovia BR-116',
        'full_name_set': {'name:prefix': 'Rodovia', 'name': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is None


def test_suffix_plus_stem_filtered(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'BR-116 Rodovia',
        'full_name_set': {'name': 'BR-116', 'name:suffix': 'Rodovia'}
    }
    result = equal_street_name_filter.process(data)
    assert result is None


def test_no_addr_street_returns_elements(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'full_name_set': {'ref': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is not None


def test_diff_prefix_ref_naming_not_flagged(
        equal_street_name_filter: EqualStreetNameFilter):
    data = {
        'street_name': 'Avenida BR-116',
        'full_name_set': {'ref': 'BR-116'}
    }
    result = equal_street_name_filter.process(data)
    assert result is None
