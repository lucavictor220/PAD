import asyncio
from Message import Message
from tinydb import TinyDB
import logging

logging.basicConfig(level="INFO",
                    format='%(levelname)s:%(message)s')


class ConsistencyService:
    def __init__(self):
        self.__DB = TinyDB('../data/db.json')

    def add(self, document):
        # TODO add validation of the document(message)
        self.__DB.insert(document)

    async def restore_queues(self, queues):
        messages = self.__restore_messages()
        if len(messages) is 0:
            logging.info('No messages stored in the Database. [restore_queues]')
            return
        for message in messages:
            topic = message.get_topic()
            if topic == '' or topic is None:
                # add to default queue
                topic = 'DEFAULT'
            if topic not in queues:
                # create queue if it is not in the already existing ones
                logging.info('Creating new queue of {0} topic... [restore_queues]'.format(topic))
                queues[topic] = asyncio.Queue(loop=asyncio.get_event_loop())

            logging.info('Adding message to {0} queue. [restore_queues]'.format(topic))
            await queues[topic].put(message.get_dictionary())
            logging.info('QUEUE {0} size is: {1}'.format(topic, queues[topic].qsize()))

    def __restore_messages(self):
        messages = []
        messages_documents = self.__DB.all()
        if len(messages_documents) == 0:
            return []
        for message_document in messages_documents:
            messages.append(Message(**message_document))

        return messages

    def check_for_existing_queues(self, queues):
        for queue_topic in queues:
            print('Queue with the topic {0} contains {1} elements'.format(queue_topic, queues[queue_topic].qsize()))
