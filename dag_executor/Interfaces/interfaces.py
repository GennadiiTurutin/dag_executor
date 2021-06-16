from abc import abstractmethod, ABC

class BaseInterface(ABC):
    def resolve(self):
        pass
    
class AWSInterface(ABC):
    def get(self):
        pass
    
    def post(self):
        pass
    
    def delete(self):
        pass