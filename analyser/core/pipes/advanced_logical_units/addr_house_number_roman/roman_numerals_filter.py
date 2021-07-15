from analyser.logger.logger import LOG
import re
from typing import List
from analyser.core.pipes.advanced_logical_units import AdvancedLogicalUnit

class AddrHouseNumberRomanNumFilter(AdvancedLogicalUnit):
    def process(self, data: List[dict]) -> List[dict]:
        """
            Filter each data result by checking if 
            the housenumber doesn't contain any digit in any scripts
            (by using the \d in python regex) and if it contains roman numerals.
        """
        filtered_data = list()
        any_digit_regex = re.compile(r'.*\d.*')
        roman_numerals_regex = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
                                """, re.VERBOSE)
        for d in data:
            #Keep only data where do not match at least one digit and where we match roman numerals.
            if not any_digit_regex.match(d['housenumber']) and roman_numerals_regex.match(d['housenumber']):
                filtered_data.append(d)
        LOG.info('After filtering there is %s results.', len(filtered_data))
        return filtered_data

