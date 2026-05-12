import uuid
class Filter():

    def __init__(self, name, regex):
        self.uuid = uuid.uuid7() 
        self.name = name
        self.regex = regex
        self.enabled = False
