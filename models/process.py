from typing import Optional

def __num_sequence_generator(seed = 1):
    """ Returns a sequence of numbers starting from a given number. """
    value = seed

    while True:
        yield value
        value += 1

class Process:
    """ Models the form of a process in an operating system. """

    id_sequence = __num_sequence_generator()

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
    def is_marked_ended(self):
        return self.__completion is not None

    @property
    def is_depleted(self):
        return self.__burst_remaining <= 0

    @property
    def is_pending(self):
        return self.__completion is None

    def tick(self, time_quantum: int = 1):
        """ Runs the process based on a given time quantum. """
        self.__burst_remaining -= time_quantum

    def end(self, timestamp: int):
        """ Marks the process as ended and records its time of completion based on a timestamp. """
        self.__completion = timestamp
        self.__turnaround = self.__completion - self.__arrival
        self.__waiting = self.__turnaround - self.__burst