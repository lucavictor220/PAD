class Message:
    def __init__(self, _to, _from, _topic='', _payload='', _type='ok'):
        self._type = _type
        self._topic = _topic
        self._from = _from
        self._to = _to
        self._payload = _payload

    def set_to(self, _to):
        self._to = _to

    def get_to(self):
        return self._to

    def set_from(self, _from):
        self._from = _from

    def set_type(self, _type):
        self._type = _type

    def get_payload(self):
        return self._payload

    def get_type(self):
        return self._type

    def get_topic(self):
        return self._topic

    def get_dictionary(self):
        return {
            '_type': self._type,
            '_from': self._from,
            '_to': self._to,
            '_topic': self._topic,
            '_payload': self._payload
        }