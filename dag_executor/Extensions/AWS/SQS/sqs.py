import json
import boto3
from dag_executor import Interfaces

class SQS(Interfaces.AWSInterface):
    def __init__(self, queue, region, max_messages=10, wait_time=10):
        self.queue_name = queue
        self.max_messages = max_messages
        self.wait_time = wait_time
        self.queue = boto3.resource(
            'sqs',
            region_name=region,
        ).get_queue_by_name(QueueName=self.queue_name)
        
    def __repr__(self):
        return 'SQS Listener to queue {}'.format(self.queue_name)
    
    def __setattr__(self, name, value):
        if not value:
            raise AttributeError('Empty value for {} not allowed'.format(name))
        if name in self.__dict__:
            raise AttributeError(
                'Changing value of {} is not allowed'.format(name))

        self.__dict__[name] = value

    def get(self):
        return self.queue.receive_messages(
            AttributeNames=['All'],
            MaxNumberOfMessages=self.max_messages,
            WaitTimeSeconds=self.wait_time
        )
        
    def post(self, message):
        return self.queue.send_message(MessageBody=json.dumps(message))
    
    def convert(self, messages=[]):
        return list(map(lambda x: json.loads(x.body), messages))
    
    @staticmethod
    def delete(messages):
        for message in messages:
            message.delete()
