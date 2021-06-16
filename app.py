from dag_executor.Executor import Executor
from dag_executor.Pipeline import Pipeline 
from dag_executor.Connector import Connector 
from dag_executor.Step import Step
from dag_executor.Function import Function 
from dag_executor.Scheduler import Scheduler
from dag_executor.Extensions.AWS import S3, SNS, SQS
import json
import uuid
import datetime as dt
import time

# Please provide your queue and buckets to test it or comment it out
queue_name = 'test_queue'
bucket_name = 'test_bucket'
aws_region = 'us-east-1'

sqs = SQS(queue_name, aws_region)
s3 = S3(bucket_name, aws_region)

execution_frequency = 30

executor = Executor()

##### PIPELINE 1 ######
step1 = Step(
    name='step #1', 
    func=Function(print, 'Starting the DAG process'), 
)

step2 = Step(
    name='step #2', 
    func=Function(lambda x, y: x/y, {'x':5, 'y':0}, '**'), 
    error_step=Step(name='step #2 on failure', func=Function(lambda x, y: x/y, {'x':5, 'y':1}, '**')),
)   

step3 = Step(
    name='step #3', 
    func=Function(print, conn=Connector(step2)) # connecting the result of step 2 and step 3 and providing it as an argument to step 3
)

pipeline1 = Pipeline(
    name='pipeline #1', 
    flow=[step1, step2, step3]
)

#### PIPELINE ON FAILURE #####
# gets triggered only if the previous pipeline failed
on_failure_pipeline = Pipeline(
    name='on_failure_pipeline', 
    flow=[Step(
        name='on_failure_step',
        func=Function(print, 'I get executed only if pipeline #1 failed')
    )]
)

##### PIPELINE 2 ###########
pipeline2 = Pipeline(
    name='pipeline #2', 
    flow=[Step(
        name='another step',
        func=Function(print, 'I get executed only if pipeline #1 succeeded')
    )]
)

###### PIPELINE # #########
pipeline3 = Pipeline(
    name='pipeline #3', 
    flow=[Step(
        name='Sending messages to SQS',
        func=Function(sqs.post, {'message': f'Test Message at {dt.datetime.now().strftime("%H:%M:%S")}'})
    ), Step(name='TimeOut 5 seconds before reading from the queue', func=Function(time.sleep, 5))
    ]
)

###### PIPELINE 4 #########
step4 = Step(name='Reading messages from SQS',func=Function(sqs.get))

step5 = Step(
    name='Converting into JSON', 
    func=Function(sqs.convert, conn=Connector(step4)), # Connecting result of step4 to step5
    error_step=Step(name='on failure step', func=Function(print, "There are no messages in the queue"))
)

step6 = Step(
    name='Displaying messages', 
    func=Function(print, conn=Connector(step5))
)

def make_files(messages=[]):
    file_names = []
    for message in messages:
        random_file_name = str(uuid.uuid4().hex) + '.json'
        with open(random_file_name, 'w') as file:
            json.dump(messages, file)
            file_names.append(random_file_name)
    return file_names
        
step7 = Step(
    name='Generating a file from SQS messages', 
    func=Function(make_files, conn=Connector(step5))
)

pipeline4 = Pipeline(
    name='pipeline #4', 
    flow=[step4, step5, step6, step7]
)

##### PIPELINE 5 ############
step8 = Step(
    name='Putting files into S3 bucket', 
    func=Function(s3.post, conn=Connector(step7))
)

step9 = Step(
    name='Displaying the status of the S3 upload', 
    func=Function(print, 'Successfully uploaded the files')
)

pipeline5 = Pipeline(
    name='pipeline #5', 
    flow=[step8, step9]
)

##### PIPELINE 6 #########

step10 = Step(
    name='Downloading the files back into the local folder', 
    func=Function(s3.get, conn=Connector(step7))
)

step11 = Step(
    name='Displaying the status of the S3 download', 
    func=Function(print, 'Successfully downloaded the files back')
)

pipeline6 = Pipeline(
    name='pipeline #6', 
    flow=[
        Step(name='TimeOut 10 seconds before reading from the bucket', func=Function(time.sleep, 10)), 
        step10, 
        step11
    ]
)

##########################
# remove pipelines 3 - 6 below if you don't have access to AWS 
def run_job():
    executor\
        .do(pipeline1)\
            .on_failure(on_failure_pipeline)\
        .do(pipeline2)\
        .do(pipeline3)\
        .do(pipeline4)\
        .do(pipeline5)\
        .do(pipeline6)\
            .on_failure(Pipeline(
                name='another on failure pipelin', 
                flow=[
                    Step(name='On Failure Step', func=Function(print, 'Failed because S3 does not show uploaded display files right away')), 
                ]
            ))\
        .finish()
##########################

scheduler = Scheduler(execution_frequency, run_job) # every 30 seconds execute function run_job.


if __name__ == '__main__':
    print("Starting the application")
    scheduler.start(run_job)
    print("Finishing the process")