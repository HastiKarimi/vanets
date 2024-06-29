
class TaskQueue:
    def __init__(self):
        self.tasks = []
        self.processing_time = 0
        self.num_tasks_processed = 0
        self.sum_queue_length = 0
        self.last_change_queue_length = 0

    def add_task(self, task, time):
        self.update_queue_length(time)
        task.arrival_time = time
        self.tasks.append(task)

    def process_next_task(self, time):
        task = self.tasks.pop(0)
        task.is_processed = True
        task.finish_time = time + task.processing_time
        task.service_start_time = time
        self.processing_time += task.processing_time
        self.num_tasks_processed += 1
        return task
    
    def update_queue_length(self, time):
        self.sum_queue_length += self.num_tasks() * (time - self.last_change_queue_length)
        self.last_change_queue_length = time

    def is_empty(self):
        return len(self.tasks) == 0
    
    def num_tasks(self):
        return len(self.tasks)
    
    def sum_priority(self):
        return sum(t.priority for t in self.tasks)
    
    def __lt__(self, ot):
        return len(self.tasks) < len(ot.tasks)