from pprint import pprint
import schedule
import time
from datetime import datetime

class Executor:
    """
    Design Pattern: singleton
    """
    __instance = None
    __slots__ = ['status', '_resolution', 'logging']
    
    def __new__(cls):
        if Executor.__instance is None:
            Executor.__instance = object.__new__(cls)
        return Executor.__instance
    
    def __init__(self):
        self.status = 'initialized'
        self._resolution = [] # {'resolutions': []}
    
    @property
    def resolution(self):
        return {'resolutions': self._resolution, 'time':  datetime.now().strftime("%d/%m/%Y %H:%M:%S")} 
    
    def reset(self):
        self.__init__()
        
    def do(self, pipeline):
        if self.status == 'failed':
            return self
        
        resolution = pipeline.resolve()
        self._resolution.append(resolution)
        self.status = resolution['status']
        return self
        
    def on_failure(self, pipeline):
        if self.status == 'failed':
            self.status = 'executed with errors'
            self.do(pipeline)
        return self
    
    def finish(self):
        # pprint(self.resolution)
        self.reset()
