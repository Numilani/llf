import uuid
import re
class Filter():

    def __init__(self, name, regex):
        self.uuid = uuid.uuid7() 
        self.name = name
        self.regex_string = regex
        self.regex_compiled = re.compile(self.regex_string)
        self.enabled = False

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "regex": self.regex_string
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> Filter:
        f = Filter(d["name"], d["regex"])
        f.uuid = d["uuid"]
        return f
