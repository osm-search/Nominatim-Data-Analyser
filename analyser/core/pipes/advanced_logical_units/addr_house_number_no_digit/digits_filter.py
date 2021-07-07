from analyser.logger.logger import LOG
import re
from typing import List
from analyser.core.pipes.advanced_logical_units import AdvancedLogicalUnit

class AddrHouseNumberNoDigitFilter(AdvancedLogicalUnit):
    def process(self, data: List[dict]) -> List[dict]:
        """
            Filter each data result by checking if 
            the housenumber contains any digit in any scripts
            (by using the \d in python regex).
        """
        filtered_data = list()
        any_digit_regex = re.compile(r'.*\d.*')
        for d in data:
            #Keep only data where me match at least one digit
            if not any_digit_regex.match(d['housenumber']):
                filtered_data.append(d)
        LOG.info('After filtering there is %s results.', len(filtered_data))
        return filtered_data

