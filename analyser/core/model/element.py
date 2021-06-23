from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

@dataclass
class Element(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def create_from_sql_result(result: any, *args) -> Element:
        """
            Return an Element based on an SQL result.
        """
        return