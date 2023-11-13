from typing import Optional

def __id_sequence(seed = 1):
    value = seed

    while True:
        yield value
        value += 1

class Process:
    id_sequence = __id_sequence()

    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int = 1, queue_level: int = 1):
        self.__pid: int = pid
        
        self.__arrival: int = arrival_time
        self.__burst: int = burst_time
        self.__burst_remaining: int = burst_time
        
        self.__priority: int = priority
        self.__queue_level: int = queue_level

        self.__completion: Optional[int] = None
        self.__turnaround: Optional[int] = None
        self.__waiting: Optional[int] = None
    
    @property 
    def pid(self):
        return self.__pid
    
    @property 
    def priority(self):
        return self.__priority
    
    @property 
    def queue_level(self):
        return self.__queue_level
    
    @property 
    def arrival(self):
        return self.__arrival
    
    @property 
    def burst(self):
        return self.__burst
 
    @property
    def burst_remaining(self):
        return self.__burst_remaining
    
    @property 
    def completion(self):
        return self.__completion
    
    @property 
    def turnaround(self):
        return self.__turnaround
    
    @property 
    def waiting(self):
        return self.__waiting
    
    @property
    def is_completed(self):
        return self.__completion is not None
    
    @property
    def is_pending(self):
        return self.__completion is None

    def tick(self, time = 1):
        self.__burst_remaining -= time

    def end(self, timestamp):
        self._completion = timestamp
        self._turnaround = self._completion - self._arrival
        self._waiting = self._turnaround - self._burst