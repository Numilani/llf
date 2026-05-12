import uuid
import re
class Filter():

    def __init__(self, name, regex):
        self.uuid = uuid.uuid7() 
        self.name = name
        self.regex_string = regex
        self.regex_compiled = re.compile(self.regex_string)
        self.enabled = False
