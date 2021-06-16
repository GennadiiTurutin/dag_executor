import json
import operator
from sys import getsizeof
from functools import reduce
import boto3
from dag_executor import Interfaces 

class SNS(Interfaces.AWSInterface):
    def __init__(self, arn, region):
        self.arn = arn
        self.client = boto3.client('sns', region_name=region)

    def __repr__(self):
        return 'SNS client with ARN {}'.format(self.arn)

    def __setattr__(self, name, value):
        if not value:
            raise AttributeError(f'Empty value for {name} not allowed')
        if name in self.__dict__:
            raise AttributeError(f'Changing value of {name} is not allowed')

        self.__dict__[name] = value
        
    def get(self):
        pass
    
    @staticmethod
    def check_size(messages):
        return int(getsizeof(json_messages)) / 1000 < 256

    def post(self, messages):
        json_messages = json.dumps(messages)
        if check_size(json_messages):
            return self.client.publish(TopicArn=self.arn, Message=json_messages)
        response = [list(self.post(messages[:len(messages)//2])),
                    list(self.post(messages[len(messages)//2:]))]

        return reduce(operator.add, response)
