from enum import Enum


class Event:
    def __init__(self, event_time, event_type, entity, processor_id=None):
        self.event_time = event_time
        self.event_type = event_type
        self.entity = entity
        self.processor_id = processor_id

    def __lt__(self, ot):
        return self.event_time < ot.event_time


class EventType(Enum):
    GENERATE_TASK = 1
    PROCESS_CONTROL_CENTER = 2
    PROCESS_PARKED_CAR = 3
    MOVE_TO_PARKED_CAR = 4
    PROCESSING_FINISHED = 5
    