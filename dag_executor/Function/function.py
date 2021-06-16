
from dag_executor import Interfaces 

class Function(Interfaces.BaseInterface): 
    __slots__ = ['function', 'args', 'args_type', 'conn']
    def __init__(self, function=None, args=None, args_type=None, conn=None):
        self.function = function
        self.args = args
        self.args_type = args_type
        self.conn = conn
    
    def __getattribute__(self, name):
        if name == 'args' and self.conn:
            return self.conn.result
        return object.__getattribute__(self, name)
    
    def resolve(self):
        if self.conn:
            self.args = self.conn.result
        if self.args_type == '*':
            return self.function(*self.args)
        elif self.args_type == '**':
            return self.function(**self.args)
        elif not self.args_type and not self.args:
            return self.function()
        return self.function(self.args)