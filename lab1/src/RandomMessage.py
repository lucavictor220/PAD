import random
import systemDefaults
from Message import Message

TOPICS = systemDefaults.TOPICS


def random_send_message():
    topic = random.choice(systemDefaults.TOPICS)
    payload = 'FACEM CEVA CU TOLK IN [{}] SHIRT'.format(topic)

    return Message(type='send', topic=topic, payload=payload)


def random_get_message():
    topic = random.choice(systemDefaults.TOPICS)

    return Message(type='get', topic=topic, payload='')


def generate_subscription_message():
    topic = random.choice(systemDefaults.TOPICS)
    return Message(type="subscribe", topic=topic)



