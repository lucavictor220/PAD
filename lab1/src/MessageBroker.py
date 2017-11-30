import asyncio
import json
import logging


from Message import Message
from Response import Response
from ConsistencyService import ConsistencyService
import systemDefaults

logging.basicConfig(level="INFO", format='%(levelname)s:%(message)s')

ConsistencyService = ConsistencyService()
TOPICS = systemDefaults.TOPICS

PERSISTENT_QUEUE = systemDefaults.PERSISTENT_QUEUE
QUEUE_MAX_SIZE = systemDefaults.QUEUE_MAX_SIZE


_QUEUES = {
    'DEFAULT': asyncio.Queue(QUEUE_MAX_SIZE, loop=asyncio.get_event_loop()),
}

_SUBSCRIBERS = {}

_TYPES_OF_RESPONSE = {
    'ERROR': 'error',
    'OK': 'ok',
    'INFO': 'info'
}

_COMMANDS = {
    'SEND': 'send',
    'GET': 'get',
    'SUBSCRIBE': 'subscribe'
}


async def handle_send(message, queue_type):
    # ensure persistence
    ConsistencyService.add(message.get_dictionary())
    logging.info('Added message to database')
    # if message has no topic store it in default queue
    if queue_type is '':
        logging.info('Message has no topic. [handle_send]')
        queue_type = 'DEFAULT'
    # if queue type doesn't exist yet, create one
    if queue_type not in _QUEUES:
        logging.info('Creating new queue with the topic {0}. [handle_send]'.format(queue_type))
        _QUEUES[queue_type] = asyncio.Queue(QUEUE_MAX_SIZE, loop=asyncio.get_event_loop())
    await _QUEUES[queue_type].put(message.get_dictionary())
    payload = 'Message added to %s queue' % queue_type

    return Response(type=_TYPES_OF_RESPONSE['OK'], payload=payload)

async def handle_get(queue_type):
    queue_type = queue_type.upper()
    logging.info('Getting message from {} queue...'.format(queue_type))
    if queue_type not in _QUEUES.keys():
        logging.info('Message topic doesn\'t exist.')
        return Response(type=_TYPES_OF_RESPONSE['ERROR'], payload='No such topic')
    if not _QUEUES[queue_type].empty():
        queue_message = await _QUEUES[queue_type].get()
        queue_message = Message(**queue_message)
        return Response(type=_TYPES_OF_RESPONSE['OK'], payload=queue_message.get_payload())

    logging.info("Queue {0} is empty. Remove: {1}".format(queue_type, PERSISTENT_QUEUE))
    if PERSISTENT_QUEUE is True:
        del _QUEUES[queue_type]
    return Response(type=_TYPES_OF_RESPONSE['ERROR'], payload='No such topic')


@asyncio.coroutine
def handle_command(message):
    command = message.get_type()
    queue_type = message.get_topic().upper()
    if command not in _COMMANDS.values():
        logging.warning('The command provided in the message doesn\'t exist.')
        return Response('ERROR', 'Wrong command')

    if command == _COMMANDS['SEND']:
        logging.info('===== SEND COMMAND START =====')
        response = yield from handle_send(message, queue_type)
        logging.info('===== SEND COMMAND END =====')
        return response

    elif command == _COMMANDS['GET']:
        logging.info('===== GET COMMAND START =====')
        response = yield from handle_get(queue_type)
        logging.info('===== GET COMMAND END =====')
        return response

    return Response(_TYPES_OF_RESPONSE['ERROR'], 'Something wrong, I don\'t really know')


@asyncio.coroutine
def handle_message(reader, writer):
    check_for_existing_queues()
    data = yield from reader.read(200)
    message = data.decode('utf-8')

    # deserialize data
    deserialized_data = json.loads(message)
    message = Message(**deserialized_data)
    logging.info('Message from the client to be processed {}'.format(message.get_dictionary()))

    response = yield from handle_command(message)
    logging.info('Response to be send to the client {}'.format(response.get_dictionary()))
    # serialize response
    serialized_response = json.dumps(response.get_dictionary())
    writer.write(serialized_response.encode('utf-8'))
    writer.write_eof()
    yield from writer.drain()
    writer.close()


def check_for_existing_queues():
    for queue_topic in _QUEUES:
        logging.info('Queue with the topic {0} contains {1} elements'.format(queue_topic, _QUEUES[queue_topic].qsize()))


def run_server(hostname='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ConsistencyService.restore_queues(_QUEUES))
    coro = asyncio.start_server(handle_message, hostname, port, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server()