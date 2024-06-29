class Task:
    def __init__(self, priority, creation_time, processing_time):
        self.priority = priority
        self.creation_time = creation_time
        self.arrival_time = 0
        self.service_start_time = 0
        self.finish_time = 0
        self.is_processed = False
        self.processing_time = processing_time

    def __lt__(self, others):
        return self.priority < others.priority
