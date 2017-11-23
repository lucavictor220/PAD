import asyncio
import json
import logging
from tinydb import TinyDB


from Message import Message
from Response import Response
from ConsistencyService import ConsistencyService
import systemDefaults

logging.basicConfig(level="INFO",
                    format='%(levelname)s:%(message)s')

ConsistencyService = ConsistencyService()
TOPICS = systemDefaults.TOPICS
RECEIVERS = systemDefaults.RECEIVERS
SENDERS = systemDefaults.SENDERS

DB = TinyDB('../data/db.json')

_ID = 0

_QUEUES_LIMIT = 10


_QUEUES = {
    'DEFAULT': asyncio.Queue(loop=asyncio.get_event_loop()),
}

_TYPES_OF_RESPONSE = {
    'ERROR': 'error',
    'OK': 'ok',
    'INFO': 'info'
}

_TYPES_OF_REQUEST = {
    'COMMAND': 'command',
}

_COMMANDS = {
    'SEND': 'send',
    'GET': 'get'
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
        _QUEUES[queue_type] = asyncio.Queue(loop=asyncio.get_event_loop())
    await _QUEUES[queue_type].put(message.get_dictionary())
    payload = 'Message added to %s queue' % queue_type

    return Response(_type=_TYPES_OF_RESPONSE['OK'], _payload=payload)

async def handle_get(message, queue_type):
    queue_type = queue_type.upper()
    logging.info('Get message from {} queue '.format(queue_type))
    if queue_type not in _QUEUES.keys():
        return Response(_type=_TYPES_OF_RESPONSE['ERROR'], _payload='No such topic')
    if not _QUEUES[queue_type].empty():
        queue_message = await _QUEUES[queue_type].get()
        queue_message = Message(**queue_message)
        logging.info('Message to be send from {0} queue {1}'.format(queue_type, queue_message.get_dictionary()))
        logging.info(message.get_to() == queue_message.get_to())
        if message.get_to() == queue_message.get_to():
            return Response(_type=_TYPES_OF_RESPONSE['OK'], _payload=queue_message.get_payload())
        else:
            return Response(_type=_TYPES_OF_RESPONSE['ERROR'], _payload='No messages for you')

    logging.info("Queue is empty")
    return Response(_type=_TYPES_OF_RESPONSE['INFO'], _payload='No messages for you')


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
        response = yield from handle_get(message, queue_type)
        logging.info('===== GET COMMAND END =====')
        return response

    return Response(_TYPES_OF_RESPONSE['ERROR'], 'Something wrong, I don\'t really know')


@asyncio.coroutine
def handle_message(reader, writer):
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


async def restore_queues():
    messages = restore_messages()
    if len(messages) is 0:
        print('No messages stored in the Database. [restore_queues]')
        return
    for message in messages:
        topic = message.get_topic()
        if topic == '' or topic is None:
            # add to default queue
            topic = 'DEFAULT'
        if topic not in _QUEUES:
            # create queue if it is not in the already existing ones
            print('Creating new queue of {0} topic... [restore_queues]'.format(topic))
            _QUEUES[topic] = asyncio.Queue(loop=asyncio.get_event_loop())

        print('Adding message to {0} queue. [restore_queues]'.format(topic))
        await _QUEUES[topic].put(message.get_dictionary())
        print(_QUEUES[topic].qsize())


def restore_messages():
    messages = []
    messages_documents = DB.all()
    if len(messages_documents) == 0:
        return []
    for message_document in messages_documents:
        messages.append(Message(**message_document))

    return messages


def check_for_existing_queues():
    for queue_topic in _QUEUES:
        print('Queue with the topic {0} contains {1} elements'.format(queue_topic, _QUEUES[queue_topic].qsize()))


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