class Response:
    def __init__(self, type, payload):
        self.type = type
        self.payload = payload

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def get_dictionary(self):
        return {
            'type': self.type,
            'payload': self.payload
        }