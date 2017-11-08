import asyncio
import json

GET_MESSAGE = {
    'type': 'get',
    'to': 'Natali',
    'payload': '',

}


@asyncio.coroutine
def get_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    # serialize data
    serialized_data = json.dumps(message)
    #write message
    writer.write(serialized_data.encode('utf-8'))

    # read message
    que_message = yield from reader.read(200)
    # deserialize data
    deserialized_data = json.loads(que_message.decode('utf-8'))

    return deserialized_data




@asyncio.coroutine
def run_receiver(loop):
    while True:
        try:
            response = yield from get_message(GET_MESSAGE, loop)
            print('Receiver: Response from que:', response)
            yield from asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_receiver(loop))