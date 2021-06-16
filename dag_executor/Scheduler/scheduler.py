import schedule

class Scheduler:
    def __init__(self, frequency, function):
        self.frequency = frequency
        self.function = function
        schedule.every(self.frequency).seconds.do(self.function)
        
    def __repr__(self):
        return f'Scheduler with frequency {self.frequency}'
    
    @staticmethod
    def start(arg):
        while True:
            schedule.run_pending()
        