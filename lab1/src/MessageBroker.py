import asyncio
import json
from tinydb import TinyDB
import ast

from Message import Message
from Response import Response

_ID = 0


_QUEUES = {
    'RED': asyncio.Queue(loop=asyncio.get_event_loop()),
    'GREEN':  asyncio.Queue(loop=asyncio.get_event_loop()),
    'BLUE': asyncio.Queue(loop=asyncio.get_event_loop())
}


db = TinyDB('../data/messages.json')
red_table = db.table('RED')
green_table = db.table('GREEN')
blue_table = db.table('BLUE')

DB_TABLES = {
    'RED': red_table,
    'GREEN': green_table,
    'BLUE': blue_table
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


@asyncio.coroutine
def handle_command(message):
    print(message.get_dictionary())
    command = message.get_type()
    if command not in _COMMANDS.values():
        print('Wrong command')
        return Response('ERROR', 'Wrong command')
    if command == _COMMANDS['SEND']:
        print('Add to que')
        # ensure persistence
        print(message.get_dictionary())
        red_table.insert(message.get_dictionary())
        yield from _QUEUES['RED'].put(message)

        return Response(_type=_TYPES_OF_RESPONSE['OK'], _payload='Added To Queue')
    elif command == _COMMANDS['GET']:
        print('Get from que')
        if not _QUEUES['RED'].empty():
            queue_message = yield from _QUEUES['RED'].get()
            queue_message = Message(**queue_message.get_dictionary())
            if message.get_to() == queue_message.get_to():
                return Response(_TYPES_OF_RESPONSE['OK'], queue_message.get_payload())
            else:
                return Message(_TYPES_OF_RESPONSE['ERROR'], 'No messages for you')
        else:
            print("que empty")
            return Response(_TYPES_OF_RESPONSE['ERROR'], 'No messages for you')

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
    yield from writer.drain()
    writer.close()


async def restore_queues():
    for name in _QUEUES:
        print(name)
        await restore_queue(name)
        if _QUEUES[name].empty():
            print("queue %s is empty" % name)

async def restore_queue(name):
    table = DB_TABLES[name]
    messages = table.all()
    [await _QUEUES[name].put(Message(**message)) for message in messages]
    print(_QUEUES[name].qsize())


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