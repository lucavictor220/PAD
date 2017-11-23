import random
import systemDefaults
from Message import Message

TOPICS = systemDefaults.TOPICS
RECEIVERS = systemDefaults.RECEIVERS
SENDERS = systemDefaults.SENDERS
NUMBER_OF_RANDOM_MESSAGES = systemDefaults.NUMBER_OF_RANDOM_MESSAGES


class RandomMessage:
    def __random_send_message(self, index):
        topic = random.choice(systemDefaults.TOPICS)
        payload = 'FACEM CEVA CU TOLK [{0}] TIMES IN [{1}] SHIRT'.format(index, topic)
        to = random.choice(RECEIVERS)
        from_ = random.choice(SENDERS)
        return Message(_type='send', _topic=topic, _payload=payload, _to=to, _from=from_)

    def generate_send_messages(self, nr_of_messages=100):
        messages = []
        for i in range(0, nr_of_messages):
            messages.append(self.__random_send_message(i))

        return messages

    def __random_get_message(self):
        topic = random.choice(systemDefaults.TOPICS)
        to = random.choice(RECEIVERS)
        from_ = random.choice(SENDERS)
        return Message(_type='get', _topic=topic, _payload='', _to=to, _from=from_)

    def generate_get_messages(self, nr_of_messages=100):
        messages = []
        for i in range(0, nr_of_messages):
            messages.append(self.__random_get_message())

        return messages
