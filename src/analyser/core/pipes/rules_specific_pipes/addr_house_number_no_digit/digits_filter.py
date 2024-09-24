from ....pipe import Pipe
from typing import Dict
import re

class AddrHouseNumberNoDigitFilter(Pipe):
    def on_created(self) -> None:
        self.any_digit_regex = re.compile(r'.*\d.*')

    def process(self, elements: Dict) -> Dict:
        """
            Filter the given data result by checking if 
            the housenumber contains any digit in any scripts
            (by using the \d in python regex).
        """
        #Keep only data where we do not match at least one digit
        if not self.any_digit_regex.match(elements['housenumber']):
            return elements
        return None

