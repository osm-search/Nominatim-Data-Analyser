from typing import Any
from ....pipe import Pipe


class EqualStreetNameFilter(Pipe):

    def process(self, elements: dict[str, Any]) -> dict[str, Any] | None:
        addr_street = elements.get('street_name', None)
        names = elements.get('full_name_set', [])
        if addr_street and isinstance(names, dict):
            if len(names) > 1:
                for key, val in names.items():
                    prefix_less = key.replace(':prefix', '')
                    if len(prefix_less) < len(key):
                        if (stem := names.get(prefix_less, None)) is not None:
                            if ' '.join((val, stem)) == addr_street:
                                return None
                    suffix_less = key.replace(':suffix', '')
                    if len(suffix_less) < len(key):
                        if (stem := names.get(suffix_less, None)) is not None:
                            if ' '.join((stem, val)) == addr_street:
                                return None

            parent_ref = names.get('ref', None)
            if parent_ref and addr_street.endswith(' ' + parent_ref):
                return None

        return elements
