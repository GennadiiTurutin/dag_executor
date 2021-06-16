class Connector:
    __slots__ = ['reference']
    def __init__(self, reference=None):
        self.reference = reference
    
    def __getattr__(self, name):
        return self.reference.__dict__[name]