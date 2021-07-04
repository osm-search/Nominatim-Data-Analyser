from dataclasses import dataclass, field

@dataclass
class Paths():
    web_path: str = field(default=None)
    local_path: str = field(default=None)