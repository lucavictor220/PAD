import asyncio
import json
import random

from Message import Message
from Response import Response
import systemDefaults

TOPICS = systemDefaults.TOPICS
RECEIVERS = systemDefaults.RECEIVERS
SENDERS = systemDefaults.SENDERS
NUMBER_OF_RANDOM_MESSAGES = systemDefaults.NUMBER_OF_RANDOM_MESSAGES


def random_message(index):
    topic = random.choice(systemDefaults.TOPICS)
    payload = 'FACEM CEVA CU TOLK [{0}] TIMES IN [{1}] SHIRT'.format(index, topic)
    to = random.choice(RECEIVERS)
    from_ = random.choice(SENDERS)
    return Message(_type='send', _topic=topic, _payload=payload, _to=to, _from=from_)


def generate_messages(nr):
    messages = []
    for i in range(0, nr):
        messages.append(random_message(i))

    return messages


@asyncio.coroutine
def send_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    serialized_data = json.dumps(message.get_dictionary())
    print(message._type)
    print('Write message: {0}'.format(serialized_data))
    writer.write(serialized_data.encode('utf-8'))
    writer.write_eof()
    # read message
    que_message = yield from reader.read(200)
    # deserialize data
    deserialized_data = json.loads(que_message.decode('utf-8'))
    response = Response(**deserialized_data)
    if response.get_type() == 'ok':
        return response
    else:
        print('Error. Something went wrong. [send_message]')
        print(response.get_type())
        return response


def check_message_have_been_send(response, messages_sent):
    if response.get_type() == 'ok':
        print('Message added sent successfully. [check_message_have_been_send]')
        messages_sent += 1

    return messages_sent


def are_messages_sent(messages_sent):
    if messages_sent == NUMBER_OF_RANDOM_MESSAGES:
        print('ALL {0} meesages have been sent successfully. [are_messages_sent]'.format(NUMBER_OF_RANDOM_MESSAGES))
    else:
        print('From {0} messages only {1} have been sent. [are_messages_sent]'.format(
            NUMBER_OF_RANDOM_MESSAGES, messages_sent)
        )


@asyncio.coroutine
def send_messages(messages, loop):
    messages_sent = 0
    for message in messages:
        response = yield from send_message(message, loop)
        print('Sender: Response from que: ', response.get_dictionary())
        messages_sent = check_message_have_been_send(response, messages_sent)
        yield from asyncio.sleep(0.2)

    are_messages_sent(messages_sent)
    loop.stop()


@asyncio.coroutine
def run_sender(loop):
    messages = generate_messages(NUMBER_OF_RANDOM_MESSAGES)
    while True:
        try:
            yield from send_messages(messages, loop)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_sender(loop))
