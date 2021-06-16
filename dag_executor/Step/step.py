import time
from datetime import timedelta
from dag_executor import Interfaces

class Step(Interfaces.BaseInterface):
    # __slots__ = ['name', 'result', 'error', 'function', 'error_step', '_execution_time', 'status']
    def __init__(self, name, func=None, error_step=None):
        self.name = name
        self.result = None
        self.error = None
        self.function = func
        self.error_step = error_step
        self._execution_time = None
        self.status = 'initialized' # 'ok', 'failed'
    
    @property
    def execution_time(self):
        return str(self._execution_time)
        
    def execute(self):
        try:
            return 'ok', self.function.resolve(), None,
        except Exception as e:
            return 'failed', None, e
        
    def resolve(self):
        start_time = time.monotonic()
        self.status, self.result, self.error = self.execute()
        if self.result:
            print("********************************************")
            print(f'------> Result of step {self.name}: {self.result}')
        end_time = time.monotonic()
        self._execution_time = timedelta(seconds=end_time - start_time)
        return self.get_resolution()
    
    def get_resolution(self):
        return {
            'name': self.name, 
            'result': self.result, 
            'status': self.status,
            'error': self.error, 
            'execution_time': self.execution_time
        }
            