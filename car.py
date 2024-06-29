import uuid
import heapq
from task_queue import TaskQueue


class Car:
    def __init__(self, id=None, is_moving=True):
        self.id = id if id is not None else uuid.uuid4()
        self.is_moving = is_moving
        self.tqueue = TaskQueue()
        # self.total_processing_time = 0
        # self.tasks_processed = 0

    def make_car_parked(self, time):
        self.tqueue.last_change_queue_length = time
        self.is_moving = False

    def add_task(self, task, time, overhead=0):
        task.processing_time += overhead
        task.arrival_time = task.creation_time + overhead
        self.tqueue.add_task(task, time)
        return task
        # heapq.heappush(self.queue, (task.priority, task))
        # return task.processing_time

    def process_task(self, time):
        if not self.tqueue.is_empty():
            task = self.tqueue.process_next_task(time)
            return task
        return None
        # if self.queue:
        #     _, task = heapq.heappop(self.queue)
        #     self.total_processing_time += task.processing_time
        #     self.tasks_processed += 1
        #     return task.processing_time
        # return None
    
    def next_task_processing_time(self, time):
        if not self.tqueue.is_empty():
            next_task = self.tqueue.tasks[0]
            next_task.service_start_time = time
            return next_task.processing_time
        return None
    
    def end_simulation(self, time):
        self.tqueue.end_simulation(time)
