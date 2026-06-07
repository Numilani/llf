import uuid
import re
from uuid import UUID
from re import Pattern
from typing import Self

class Filter():

    def __init__(self, name, regex):
        self.uuid: UUID = uuid.uuid7() 
        self.name: str = name
        self.regex_string: str = regex
        self.regex_compiled: Pattern = re.compile(self.regex_string)
        self.enabled: bool = False

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "regex": self.regex_string
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> Self:
        f = Filter(d["name"], d["regex"])
        f.uuid = d["uuid"]
        return f

    @classmethod
    def from_filter(cls, name, regex, uuid) -> Self:
        f = Filter(name, regex)
        f.uuid = uuid
        return f

