import asyncio
import json
import logging

from Message import Message
from Response import Response
from RandomMessage import RandomMessage


NUMBER_OF_RANDOM_MESSAGES = 100

logging.basicConfig(level="INFO",
                    format='%(levelname)s:%(message)s')


@asyncio.coroutine
def get_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    # serialize data
    serialized_data = json.dumps(message.get_dictionary())
    print(serialized_data)

    #write message
    writer.write(serialized_data.encode('utf-8'))

    # read message
    queue_message = yield from reader.read(200)
    logging.info(queue_message.decode('utf-8'))
    # deserialize data
    deserialized_data = json.loads(queue_message.decode('utf-8'))
    response = Response(deserialized_data['_type'], deserialized_data['_payload'])
    logging.info(response.get_dictionary())

    return response


@asyncio.coroutine
def send_messages(messages, loop):
    for message in messages:
        response = yield from get_message(message, loop)
        logging.info('Receiver: Response from que: {}'.format(response.get_dictionary()))
        yield from asyncio.sleep(0.3)

    loop.stop()


@asyncio.coroutine
def run_receiver(loop):
    messages = RandomMessage().generate_get_messages(NUMBER_OF_RANDOM_MESSAGES)
    while True:
        try:
            yield from send_messages(messages, loop)
            yield from asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_receiver(loop))