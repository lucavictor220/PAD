class Response:
    def __init__(self, _type, _payload):
        self._type = _type
        self._payload = _payload

    def set_type(self, _type):
        self._type = _type

    def get_type(self):
        return self._type

    def get_dictionary(self):
        return {
            '_type': self._type,
            '_payload': self._payload
        }