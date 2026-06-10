from typing import Any
from ....pipe import Pipe


def is_equal_with_affix(addr_street: str, names: dict[str, str]) -> bool:
    """ Check if a combination of *:prefix or *:suffix with a name
        returns a name that is equal to the street name.
    """
    if addr_street and len(names) > 1:
        for key, val in names.items():
            prefix_less = key.replace(':prefix', '')
            if len(prefix_less) < len(key):
                if (stem := names.get(prefix_less, None)) is not None:
                    if ' '.join((val, stem)) == addr_street:
                        return True
            suffix_less = key.replace(':suffix', '')
            if len(suffix_less) < len(key):
                if (stem := names.get(suffix_less, None)) is not None:
                    if ' '.join((stem, val)) == addr_street:
                        return True

    return False


def is_brazilian_highway(cc: str, addr_street: str, names: dict[str, str]) -> bool:
    """ If the address is in Brazil, check if the street name of
        the address refers to a highway.
    """
    if cc == 'br':
        ref = names.get('ref')
        if ref and addr_street.startswith('Rodovia ') and addr_street[8:] == ref:
            return True

    return False


class EqualStreetNameFilter(Pipe):

    def process(self, elements: dict[str, Any]) -> dict[str, Any] | None:
        addr_street = elements.get('street_name', '')
        names = elements.get('full_name_set', {})

        if is_equal_with_affix(addr_street, names):
            return None

        cc = elements.get('country_code', '')

        if is_brazilian_highway(cc, addr_street, names):
            return None

        return elements
