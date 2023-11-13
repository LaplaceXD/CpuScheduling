from typing import List
from models import ExecutionFrame

class ExecutionTrail:
    """ A class that keeps track of a list of execution frames, and trails them successively. """
    
    def __init__(self, start_at: int = 0):
        self.__start_time = start_at
        self.__trail: List[ExecutionFrame] = []

    @property
    def trail(self):
        return self.__trail

    @property
    def start_time(self):
        return self.__start_time

    @property
    def last_execution_end_time(self):
        return self.__start_time if len(self.__trail) == 0 else self.__trail[-1].end

    def add_frame(self, name: str, timestamp: int):
        """ Add a frame to the execution trail and its corresponding timestamp. """
        frame = ExecutionFrame(name, self.last_execution_end_time, timestamp)
        self.__trail.append(frame)