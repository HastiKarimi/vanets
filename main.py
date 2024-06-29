import numpy as np
from task import Task
from event import Event, EventType
from control_center import ControlCenter
from car import Car
import heapq


np.random.seed(42)
event_queue = []

PRINT_SCHEDULINGS = False
PRINT_HEAP_STATS = False


def schedule_event(event_time, event_type, entity, processor_id=None):
    if PRINT_SCHEDULINGS:
        print("-------------------------------")
        print(
            f"Scheduling event: event_time={event_time}, event_type={event_type}, entity={entity},"
            f" processor_id={processor_id} "
        )
        print("-------------------------------")
    heapq.heappush(event_queue, Event(event_time, event_type, entity, processor_id))
    if PRINT_HEAP_STATS:
        print("-------------------------------")
        print(f"heapq:")
        for e in event_queue:
            print(f"  {e.event_time}, {e.event_type}, {e.entity}, {e.processor_id}")
        print("-------------------------------")


def generate_task(current_time, lambda_1, X, entity=None):
    priority = np.random.choice([1, 2, 3], p=[0.3, 0.4, 0.3])
    processing_time = np.random.exponential(1 / lambda_1)
    task = Task(priority, current_time, processing_time)
    interarrival_time = np.random.exponential(1 / X)
    schedule_event(current_time + interarrival_time, EventType.GENERATE_TASK, entity)
    return task


def simulate(lambda_1, lambda_2, X, C, t, T, N, P, strategy):
    print("Starting Simulation.")
    # Initializing entities
    control_center = ControlCenter(num_processors=N)
    cars = [Car(id=i) for i in range(3)]
    parked_car = None

    # Schedule the first task generation event for each car
    for car in cars:
        schedule_event(0, EventType.GENERATE_TASK, car)

    # Main simulation loop
    current_time = 0
    while current_time < T and event_queue:
        event = heapq.heappop(event_queue)
        current_time = event.event_time
        if current_time > T:
            break

        print(
            f"Event which is currently being processed: {event.event_time}, {event.event_type},"
            f" {event.entity}, {event.processor_id}"
        )

        if current_time >= t and parked_car is None:
            parked_car = np.random.choice(cars)
            parked_car.is_moving = False
            print(
                f"Car {parked_car.id} is in parked state at time {current_time} and is serving tasks"
            )

        if event.event_type == EventType.GENERATE_TASK:
            task = generate_task(current_time, lambda_1, X, event.entity)
            # print( f"Received task with priority {task.priority} at time {current_time} and processing time {
            # task.processing_time}" )

            if parked_car and current_time >= t and np.random.rand() < P:
                schedule_event(
                    current_time, EventType.MOVE_TO_PARKED_CAR, parked_car, task
                )
            else:
                processor_id = control_center.add_task(task, current_time, strategy)
                if processor_id is not None:
                    # if the task is the only task in the queue, then process it
                    if control_center.task_queues[processor_id].num_tasks() == 1:
                        processing_time = control_center.process_tasks(processor_id, current_time)
                        if processing_time:
                            schedule_event(
                                current_time + processing_time,
                                EventType.PROCESSING_FINISHED,
                                control_center,
                                processor_id,
                            )
        #             schedule_event(
        #                 current_time,
        #                 EventType.PROCESS_CONTROL_CENTER,
        #                 control_center,
        #                 processor_id,
        #             )

        # elif event.event_type == EventType.PROCESS_CONTROL_CENTER:
        #     processing_time = control_center.process_tasks(event.processor_id, current_time)
        #     if processing_time:
        #         schedule_event(
        #             current_time + processing_time,
        #             EventType.PROCESSING_FINISHED,
        #             control_center,
        #             event.processor_id,
        #         )

        elif event.event_type == EventType.PROCESSING_FINISHED:
            if event.processor_id is not None:
                if not control_center.task_queues[event.processor_id].is_empty():
                    processing_time = control_center.process_tasks(event.processor_id, current_time)
                    if processing_time:
                        schedule_event(
                            current_time + processing_time,
                            EventType.PROCESSING_FINISHED,
                            control_center,
                            event.processor_id,
                        )
                else:
                    print(
                        f"error: Processor {event.processor_id} has no tasks to process at time {current_time}"
                    )
            else:
                if parked_car and parked_car.queue:
                    processing_time = parked_car.process_task(current_time)
                    if processing_time:
                        schedule_event(
                            current_time + processing_time,
                            EventType.PROCESSING_FINISHED,
                            parked_car,
                        )

        elif event.event_type == EventType.MOVE_TO_PARKED_CAR:
            parked_car.add_task(event.processor_id, current_time, C)
            if parked_car.queue:
                schedule_event(current_time, EventType.PROCESS_PARKED_CAR, parked_car)

        elif event.event_type == EventType.PROCESS_PARKED_CAR:
            processing_time = parked_car.process_task(current_time)
            if processing_time:
                schedule_event(
                    current_time + processing_time,
                    EventType.PROCESSING_FINISHED,
                    parked_car,
                )

    print("Simulation Completed!")
    # TODO: Print statistics (average lens, CDF, ...)


if __name__ == "__main__":
    lambda_1 = 0.5
    lambda_2 = 0.5
    X = 0.5
    C = 0.75
    t = 3
    T = 10
    N = 3
    P = 0.5
    strategy = "FIFO"
    simulate(lambda_1, lambda_2, X, C, t, T, N, P, strategy)
