import random
import systemDefaults
from Message import Message

TOPICS = systemDefaults.TOPICS
RECEIVERS = systemDefaults.RECEIVERS
SENDERS = systemDefaults.SENDERS
NUMBER_OF_RANDOM_MESSAGES = systemDefaults.NUMBER_OF_RANDOM_MESSAGES


class RandomMessage:
    def __init__(self, nr_of_messages=100):
        self.__nr_of_messages = nr_of_messages

    def __random_message(self, index):
        topic = random.choice(systemDefaults.TOPICS)
        payload = 'FACEM CEVA CU TOLK [{0}] TIMES IN [{1}] SHIRT'.format(index, topic)
        to = random.choice(RECEIVERS)
        from_ = random.choice(SENDERS)
        return Message(_type='send', _topic=topic, _payload=payload, _to=to, _from=from_)

    def generate_messages(self):
        messages = []
        for i in range(0, self.__nr_of_messages):
            messages.append(self.__random_message(i))

        return messages
