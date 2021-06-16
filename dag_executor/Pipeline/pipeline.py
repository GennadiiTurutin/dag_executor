
from dag_executor import Interfaces 

class Pipeline(Interfaces.BaseInterface):
    __slots__ = ['name', 'steps', 'result', 'error', 'status', 'steps_resolutions']
    def __init__(self, name, flow=[]):
        self.name = name
        self.steps = flow
        self.result = None
        self.error = None
        self.status = 'initialized'
        self.steps_resolutions = []
    
    def __repr__(self):
        return f'Pipeline: {self.show()}'
    
    def execute_step(self, step):
        resolution = step.resolve()
        self.steps_resolutions.append(resolution)
        if resolution['status'] == 'ok':
            self.status = 'ok'
        if resolution['status'] == 'failed':
            self.status = 'failed'
            self.error = resolution['error']
            print(f'Step {step.name} failed')
            if step.error_step:
                print(f'Starting execution of the corresponding step on failure {step.error_step.name}')
                self.execute_step(step.error_step)
                step.result = step.error_step.result
        
    def execute(self):
        for step in self.steps:
            print('#######################################')
            print(f'----> Starting execution of step {step.name}')
            self.execute_step(step)
            print(f'----> Finished execution of step {step.name} within {step.execution_time}')
            if self.status == 'failed':
                break
    
    def resolve(self):
        print('============================================')
        print(f'-> Starting execution of pipeline {self.name}')
        self.status = 'ok'
        self.execute() 
        print(f'-> Finishing execution of pipeline {self.name} with status {self.status}')
        if self.error:
            print(f'-> Error {self.error}')
        return {
            'name': self.name, 
            'steps': self.steps_resolutions,
            'status': self.status
        }
    
    def show(self):
        return {
            'name': self.name,
            'steps': [step.get_resolution() for step in self.steps],
            'result': self.result,
            'error': self.error,
            'status': self.status,
            'resolutions': self.steps_resolutions
        }