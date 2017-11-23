import asyncio
import json
from tinydb import TinyDB

from Message import Message
from Response import Response
import systemDefaults


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
    'OK': 'ok'
}

_TYPES_OF_REQUEST = {
    'COMMAND': 'command',
}

_COMMANDS = {
    'SEND': 'send',
    'GET': 'get'
}


async def handle_send(message, queue_type):
    print('Add to que')
    # ensure persistence
    DB.insert(message.get_dictionary())
    print(message.get_dictionary())
    # if message has no topic store it in default queue
    if queue_type is '':
        print('Message has no topic. [handle_send]')
        queue_type = 'DEFAULT'
    # if queue type doesn't exist yet, create one
    if queue_type not in _QUEUES:
        print('Creating new queue with the topic {0}. [handle_send]'.format(queue_type))
        _QUEUES[queue_type] = asyncio.Queue(loop=asyncio.get_event_loop())
    await _QUEUES[queue_type].put(message.get_dictionary())
    payload = 'Message added to %s queue' % queue_type

    return Response(_type=_TYPES_OF_RESPONSE['OK'], _payload=payload)

async def handle_get(message, queue_type):
    print('Get from que')
    queue_type = queue_type.upper()
    if queue_type not in _QUEUES.keys():
        return Response(_type=_TYPES_OF_RESPONSE['ERROR'], _payload='No such topic')
    if not _QUEUES[queue_type].empty():
        queue_message = await _QUEUES[queue_type].get()
        queue_message = Message(**queue_message.get_dictionary())
        if message.get_to() == queue_message.get_to():
            return Response(_type=_TYPES_OF_RESPONSE['OK'], _payload=queue_message.get_payload())
        else:
            return Message(_type=_TYPES_OF_RESPONSE['ERROR'], _payload='No messages for you', _topic=queue_type)
    else:
        print("que empty")
        return Response(_type=_TYPES_OF_RESPONSE['ERROR'], _payload='No messages for you')


@asyncio.coroutine
def handle_command(message):
    print(message.get_dictionary())
    command = message.get_type()
    queue_type = message.get_topic().upper()
    if command not in _COMMANDS.values():
        print('Wrong command')
        return Response('ERROR', 'Wrong command')
    if command == _COMMANDS['SEND']:
        response = yield from handle_send(message, queue_type)
        return response
    elif command == _COMMANDS['GET']:
        response = yield from handle_get(message, queue_type)
        return response

    return Response(_TYPES_OF_RESPONSE['ERROR'], 'Something wrong, I don\'t really know')


@asyncio.coroutine
def handle_message(reader, writer):
    print('handle message')
    data = yield from reader.read(200)
    message = data.decode('utf-8')

    # deserialize data
    deserialized_data = json.loads(message)
    message = Message(**deserialized_data)

    response = yield from handle_command(message)
    print('Message:')
    print(response.get_dictionary())
    # serialize response
    serialized_response = json.dumps(response.get_dictionary())
    print(serialized_response)
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
    print("restore database")
    loop.run_until_complete(restore_queues())
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