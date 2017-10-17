import asyncio
import json

MESSAGE = {
    'type': 'send',
    'payload': 'FACEM CEVA CU TOLK'
}

random_message = 'Ceva cu tolk'


@asyncio.coroutine
def send_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    serialized_data = json.dumps(MESSAGE)

    print('Write message: {0}'.format(serialized_data))
    writer.write(serialized_data.encode('utf-8'))

    data = yield from reader.read(200)
    print(data.decode())


@asyncio.coroutine
def run_sender(loop):
    while True:
        try:
            response = yield from send_message(MESSAGE, loop)
            print('Response from que:', response)
            yield from asyncio.sleep(2)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_sender(loop))
