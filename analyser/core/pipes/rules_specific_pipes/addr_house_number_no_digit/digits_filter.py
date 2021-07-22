from analyser.core.pipe import Pipe
from typing import List
import re

class AddrHouseNumberNoDigitFilter(Pipe):
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
        self.log(f'After filtering there is {len(filtered_data)} results.')
        return filtered_data

