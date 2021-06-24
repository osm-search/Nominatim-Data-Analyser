from __future__ import annotations
from .element import Element
from dataclasses import dataclass, field

@dataclass
class AdditionalData(Element):
    """
        Represents an additionnal date represented by a value
        and a code.
    """
    data: any
    code: str = field(default=None)

    def create_from_sql_result(result: any, *args) -> AdditionalData:
        """
            Return an AdditionalData based on an SQL result.
        """
        return AdditionalData(result, *args)