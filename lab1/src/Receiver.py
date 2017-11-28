import asyncio
import json
import logging

from Response import Response
import RandomMessage


logging.basicConfig(level="INFO", format='%(levelname)s:%(message)s')


@asyncio.coroutine
def get_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    logging.info("I'm ready to receive the message")
    # serialize data
    serialized_data = json.dumps(message.get_dictionary())

    #write message
    writer.write(serialized_data.encode('utf-8'))

    # read message
    queue_message = yield from reader.read()
    # deserialize data
    deserialized_data = json.loads(queue_message.decode('utf-8'))
    response = Response(deserialized_data['type'], deserialized_data['payload'])

    return response


@asyncio.coroutine
def run_receiver(loop):
    logging.info("RUNN")
    while True:
        try:
            message = RandomMessage.random_get_message()
            response = yield from get_message(message, loop)
            logging.info("Received message {}".format(response.get_dictionary()))
            yield from asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_receiver(loop))