from task_queue import TaskQueue


class ControlCenter:
    def __init__(self, num_processors=1):
        self.num_processors = num_processors
        self.task_queues = [TaskQueue() for _ in range(num_processors)]
        self.processing_time = [0] * num_processors
        self.tasks_processed = [0] * num_processors

    def add_task(self, task, time, strategy="FIFO"):
        if strategy == "FIFO":
            min_tqueue = min(self.task_queues)
            processor_id = self.task_queues.index(min_tqueue)
            min_tqueue.add_task(task, time)
        elif strategy == "NPPS":
            min_tqueue = min(self.task_queues, key=lambda tq: tq.sum_priority())
            processor_id = self.task_queues.index(min_tqueue)
            min_tqueue.add_task(task, time)
        elif strategy == "WRR":
            processor_id = int(task.creation_time % self.num_processors)
            self.task_queues[processor_id].add_task(task, time)
        else:
            raise NotImplementedError(f"Unknown strategy: {strategy}")

        return processor_id

    def process_tasks(self, processor_id, time):
        if not self.task_queues[processor_id].is_empty():
            tq = self.task_queues[processor_id]
            task = tq.process_next_task(time)
            return task
        return None
    
    def next_task_processing_time(self, processor_id, time):
        if not self.task_queues[processor_id].is_empty():
            next_task = self.task_queues[processor_id].tasks[0]
            next_task.service_start_time = time
            return next_task.processing_time
        return None
    
    def end_simulation(self, time):
        for tq in self.task_queues:
            tq.end_simulation(time)
