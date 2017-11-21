import asyncio
import json

from Message import Message
from Response import Response


my_message = Message(_type='send', _topic='RED', _payload='FACEM CEVA CU TOLK', _to='Nicolae', _from='Diana')

@asyncio.coroutine
def send_message(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    serialized_data = json.dumps(message.get_dictionary())
    print(message._type)
    print('Write message: {0}'.format(serialized_data))
    writer.write(serialized_data.encode('utf-8'))
    # read message
    que_message = yield from reader.read(200)
    # deserialize data
    deserialized_data = json.loads(que_message.decode('utf-8'))
    response = Response(**deserialized_data)
    if response.get_type() == 'ok':
        return response
    else:
        print('Something went wrong')
        print(response.get_type())
        return response


@asyncio.coroutine
def run_sender(loop):
    while True:
        try:
            response = yield from send_message(my_message, loop)
            print('Sender: Response from que:', response.get_dictionary())
            yield from asyncio.sleep(2)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(run_sender(loop))
