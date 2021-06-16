import os
import sys
import unittest
import datetime
from datetime import datetime
from datetime import timedelta
import pytz
import responses
# Rewiring path system
sys.path[0] = os.getcwd()
from tests.test_samples import resolution_sample
from dag_executor import Executor, Pipeline, Step, Function, Connector, Scheduler

def handler(x):
    return 2*x
def another_handler(x):
    return 2*x
def divide(x):
    print(x[0])
    
step1 = Step(
    name='first step', 
    func=Function(divide, {'First step'}),
    error_step=Step(name='error step', func=Function(print,'First step contingency')), 
)

step3 = Step(
    name='third step', 
    func=Function(handler, 'Third step')
)

connector = Connector(step3)

step4 = Step(
    name='fourth step', 
    func=Function(another_handler, conn=connector)
)

pipeline1 = Pipeline(
    name='pipeline1', 
    flow=[step1, step3]
)

pipeline4 = Pipeline(
    name='pipeline4', 
    flow=[step4]
)

on_failure_pipeline = Pipeline(
    name='on_failure_pipeline', 
    flow=[Step(
        name='on_failure_step',
        func=Function(print, 'Failure')
    )]
)


class MyTest(unittest.TestCase):

    # Executor
    def test_reset(self):
        pass
    
    def test_do(self):
        pass
    
    def test_on_failure(self):
        pass
        
    # Connector
    def test_get_attr_connector(self):
        pass
    
    # Function
    def test_resolve(self):
        pass
    
    def test_get_attr_function(self):
        pass
    
    # Pipeline
    def test_execute(self):
        pass
    
    def test_execute_step(self):
        pass
    
    def test_resolve(self):
        pass
    
    def test_show(self):
        pass
    
    def test_remove(self):
        pass
    
    def test_combine(self):
        pass
    
    # Step
    def test_execute(self):
        pass
    
    def test_resolve(self):
        pass
    
    def get_resolution(self):
        pass
    
    
