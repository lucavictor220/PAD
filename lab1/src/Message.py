class Message:
    def __init__(self, topic='', payload='', type='ok'):
        self.topic = topic
        self.type = type
        self.payload = payload

    def set_type(self, type):
        self.type = type

    def get_payload(self):
        return self.payload

    def get_type(self):
        return self.type

    def get_topic(self):
        return self.topic

    def get_dictionary(self):
        return {
            'type': self.type,
            'topic': self.topic,
            'payload': self.payload
        }