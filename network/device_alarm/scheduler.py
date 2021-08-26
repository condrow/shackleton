import datetime

class Schedule:

    def __init__(self):
        
        self.now = datetime.datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")

    def schedule(self, start="22:00:00", end="03:00:00"):

        dt = datetime.datetime.strptime(start,"%H:%M:%S").time()
        
        if self.current_time > start or self.current_time < end:
            return True
        else:
            return False
        


