import asyncio
import json
import logging

from Response import Response
import systemDefaults
from RandomMessage import RandomMessage


NUMBER_OF_RANDOM_MESSAGES = systemDefaults.NUMBER_OF_RANDOM_MESSAGES
logging.basicConfig(level="INFO", format='%(levelname)s:%(message)s')


@asyncio.coroutine
def send_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    serialized_data = json.dumps(message.get_dictionary())
    logging.info('Write message: {0}'.format(serialized_data))
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
        logging.error('Something went wrong. [send_message]'.format(response.get_dictionary()))
        return response


def check_message_have_been_send(response, messages_sent):
    if response.get_type() == 'ok':
        logging.info('Message added sent successfully. [check_message_have_been_send]')
        messages_sent += 1

    return messages_sent


def are_messages_sent(messages_sent):
    if messages_sent == NUMBER_OF_RANDOM_MESSAGES:
        logging.info('ALL {0} meesages have been sent successfully. [are_messages_sent]'.format(NUMBER_OF_RANDOM_MESSAGES))
    else:
        logging.warning('From {0} messages only {1} have been sent. [are_messages_sent]'.format(
            NUMBER_OF_RANDOM_MESSAGES, messages_sent)
        )


@asyncio.coroutine
def send_messages(messages, loop):
    messages_sent = 0
    for message in messages:
        response = yield from send_message(message, loop)
        logging.info('Sender: Response from que: ', response.get_dictionary())
        messages_sent = check_message_have_been_send(response, messages_sent)
        yield from asyncio.sleep(0.2)

    are_messages_sent(messages_sent)
    loop.stop()


@asyncio.coroutine
def run_sender(loop):
    messages = RandomMessage().generate_send_messages(NUMBER_OF_RANDOM_MESSAGES)
    while True:
        try:
            yield from send_messages(messages, loop)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_sender(loop))
