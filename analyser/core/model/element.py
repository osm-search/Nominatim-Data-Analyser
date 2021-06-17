from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from geojson.feature import Feature

@dataclass
class Element(metaclass=ABCMeta):
    properties: dict()

    @abstractmethod
    def to_geojson_feature(self, id: int) -> Feature:
        return

    @staticmethod
    @abstractmethod
    def create_from_sql_result(result: any) -> Element:
        """
            Return an Element based on an SQL result.
        """
        return