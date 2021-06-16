# dag_executor
The DAG Executor is the package that executes graphs that can have multiple paths of execution.

# DESCRIPTION

- Executor: manages the execution process
- Scheduler: schedules execution processes on a regular basis
- Function: a wrapper around the actual function execution. Can be connected to the output of another function through connectors
- Step: a logical unit of execution
- Pipeline: the entire process that consists of steps. 
- SNS: SNS client connected through the Facade pattern with boto3
- SQS: SQS client connected through the Facade pattern with boto3
- S3: S3 client connected through the Facade pattern with boto3
- Interfaces: help make sure that methods are implemented

# HOW TO RUN 
1. Install virtualenv: pipe install virtualenv
2. Create a new virtual environment: virtualenv venv
3. Activate the virtual environment: virtualenv source/bin/activate
4. Install the necessary dependencies: pip install -r requirements.txt
5. Start the python process: python app.py (or python3 app.py)

# REQUIREMENTS
If you need to run dag_executor with AWS services you need to have a credentials file in you home directory on Mac. 
~/aws/credentials:

```
[default]
aws_access_key=....
aws_secret_access_key=....
```

