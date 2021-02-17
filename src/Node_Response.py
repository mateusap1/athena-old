class Node_Response(object):

    def __init__(self, success, content, message):
        self.success = success # Boolean
        self.content = content
        self.message = message