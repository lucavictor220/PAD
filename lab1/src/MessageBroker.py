import asyncio
import json




@asyncio.coroutine
def handle_message(reader, writer):
    print('handle message')
    data = yield from reader.read(200)
    message = data.decode('utf-8')

    # deserialize data
    deserialized_data = json.loads(message)


    print(deserialized_data['type'])
    writer.write('Paka'.encode('utf-8'))
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