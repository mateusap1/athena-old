class Node_Request(object):

    def __init__(self, command: str, params = {}):
        self.command = command
        self.params = params