import os
import json
import boto3
from dag_executor import Interfaces 

class S3(Interfaces.AWSInterface):
    def __init__(self, bucket, region):
        self.client = boto3.client('s3', region_name=region)
        self.bucket = bucket

    def __repr__(self):
        return 'S3 Manager for bucket {}'.format(self.bucket)
    
    def __setattr__(self, name, value):
        if not value:
            raise AttributeError('Empty value for {} not allowed'.format(name))
        if name in self.__dict__:
            raise AttributeError(
                'Changing value of {} is not allowed'.format(name))

        self.__dict__[name] = value

    def delete(self, file):
        return self.client.delete_object(Bucket=self.bucket, Key=file)

    def get(self, files=[]):
        return [self.client.download_file(file, self.bucket, file) for file in files if file]

    def post(self, files=[]):
        return [self.client.upload_file(file, self.bucket, file) for file in files if file] 
