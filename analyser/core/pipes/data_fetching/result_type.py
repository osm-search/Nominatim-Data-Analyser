from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class ResultType():
    str_type: str
    additional_arguments: List[any] = field(compare=False, default_factory=list)