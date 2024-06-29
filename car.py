import uuid
import heapq


class Car:
    def __init__(self, id=None, is_moving=True):
        self.id = id if id is not None else uuid.uuid4()
        self.is_moving = is_moving
        self.queue = []
        self.total_processing_time = 0
        self.tasks_processed = 0

    def add_task(self, task, time, overhead=0):
        task.processing_time += overhead
        heapq.heappush(self.queue, (task.priority, task))
        return task.processing_time

    def process_task(self, time):
        if self.queue:
            _, task = heapq.heappop(self.queue)
            self.total_processing_time += task.processing_time
            self.tasks_processed += 1
            return task.processing_time
        return None
