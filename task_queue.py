
class TaskQueue:
    def __init__(self):
        self.tasks = []
        # sum duration of all tasks in the processor
        self.busy_time = 0
        # sum duration of all tasks in the queue
        self.queue_time = 0
        self.num_tasks_processed = 0

        # average queue length metric
        self.sum_queue_length = 0
        self.last_change_queue_length = 0

    def add_task(self, task, time):
        self.update_queue_length(time)
        task.arrival_time = time
        self.tasks.append(task)

    def process_next_task(self, time):
        self.update_queue_length(time)

        task = self.tasks.pop(0)
        task.is_processed = True
        task.finish_time = time

        self.queue_time += task.service_start_time - task.creation_time
        self.busy_time += task.processing_time
        self.num_tasks_processed += 1
        return task
    
    def update_queue_length(self, time):
        self.sum_queue_length += self.num_tasks() * (time - self.last_change_queue_length)
        self.last_change_queue_length = time

    def end_simulation(self, time):
        self.update_queue_length(time)
        for task in self.tasks:
            self.queue_time += time - task.creation_time

    def get_metrics(self):
        return {
            "queue_time": self.queue_time,
            "busy_time": self.busy_time,
            "num_tasks_processed": self.num_tasks_processed,
            "sum_queue_length": self.sum_queue_length,
        }

    def is_empty(self):
        return len(self.tasks) == 0
    
    def num_tasks(self):
        return len(self.tasks)
    
    def sum_priority(self):
        return sum(t.priority for t in self.tasks)
    
    def __lt__(self, ot):
        return len(self.tasks) < len(ot.tasks)