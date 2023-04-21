from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __lt__(self, other):
        if self.length == other.length:
            return self.name < other.name
        else:
            return self.length < other.length

    def __gt__(self, other):
        if self.length == other.length:
            return self.name > other.name
        else:
            return self.length > other.length

    def __le__(self, other):
        if self.length == other.length:
            return self.name <= other.name
        else:
            return self.length < other.length

    def __ge__(self, other):
        if self.length == other.length:
            return self.name >= other.name
        else:
            return self.length > other.length
