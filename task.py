from datetime import datetime

class Task:
    total_time = 0
    date = datetime.now()

    def __init__(self, name, start, end, color):
        self.name = name
        self.start = start
        self.end = end
        self.color = color

    def get_time(self):
        self.total_time = self.end - self.start