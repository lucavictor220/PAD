import asyncio
import json


_MESSAGE_QUEUE = asyncio.Queue(loop=asyncio.get_event_loop())

_TYPES_OF_RESPONSE = {
    'COMMAND': 'command',
    'ERROR': 'error',
    'OK': 'ok'
}

_COMMANDS = {
    'SEND': 'send',
    'GET': 'get'
}


@asyncio.coroutine
def handle_command(command, payload):
    response = {
        'type': _TYPES_OF_RESPONSE['OK'],
        'payload': 'Nica'
    }

    if command not in _COMMANDS:
        print('Wrong command')
        response['type'] = _TYPES_OF_RESPONSE['ERROR']
        response['payload'] = 'Wrong command'
    if command == _COMMANDS['SEND']:
        print('Add to que')
        yield from _MESSAGE_QUEUE.put(payload)
        response['type'] = _TYPES_OF_RESPONSE['OK']
        response['payload'] = 'Message added'
    elif command == 'get':
        print('Get from que')
        message = yield from _MESSAGE_QUEUE.get()
        response['type'] = _TYPES_OF_RESPONSE['COMMAND']
        response['payload'] = message
    else:
        print('Add error')
        response['type'] = _TYPES_OF_RESPONSE['ERROR']
        response['payload'] = 'Something wrong, I don\'t really know'

    return response


@asyncio.coroutine
def handle_message(reader, writer):
    print('handle message')
    data = yield from reader.read(200)
    message = data.decode('utf-8')

    # deserialize data
    deserialized_data = json.loads(message)

    print(deserialized_data)

    response = yield from handle_command(deserialized_data['type'], deserialized_data['payload'])
    # serialize response
    serialized_response = json.dumps(response)
    writer.write(serialized_response.encode('utf-8'))
    yield from writer.drain()
    writer.close()


def run_server(hostname='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_message, hostname, port, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('Press Ctrl + C to stop the application')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server()