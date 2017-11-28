import asyncio
import json
import logging

from Response import Response
import systemDefaults
import RandomMessage

NUMBER_OF_RANDOM_MESSAGES = systemDefaults.NUMBER_OF_RANDOM_MESSAGES
logging.basicConfig(level="INFO", format='%(levelname)s:%(message)s')


@asyncio.coroutine
def send_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)
    logging.info(writer.get_extra_info('peername'))

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


def check_message_have_been_send(response):
    if response.get_type() == 'ok':
        logging.info('Message sent successfully. [check_message_have_been_send]')
    else:
        logging.info('Failed to add message to queue. [check_message_have_been_send]')


@asyncio.coroutine
def run_sender(loop):
    while True:
        try:
            message = RandomMessage.random_send_message()
            response = yield from send_message(message, loop)
            check_message_have_been_send(response)
            yield from asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_sender(loop))
