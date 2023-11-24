from typing import List, Callable
from abc import ABC, abstractmethod

from models import Process
from modules import Processor

class Scheduler(ABC):
    name: str = "Scheduler"
    is_priority_required: bool = False
    is_queue_level_required: bool = False

    def __init__(self, processes: List[Process], processor: Processor):
        self._processes: List[Process] = processes
        self._processor: Processor = processor
        self._ready_queue: List[Process] = []

    def __str__(self):
        return self.name
    
    @classmethod
    def is_instance(cls, scheduler_instance: 'Scheduler'):
        """ Checks whether a given instance is an instance of this scheduler class. """
        return cls.name == scheduler_instance.name
    
    @classmethod
    def create(cls):
        """ A method that returns a partially instantiated scheduler that can be latched onto the operating system for use. """
        partialized_instance: Callable[[List[Process], Processor], cls] = lambda pl, p : cls(pl, p)
        return partialized_instance

    @property
    def waiting_queue(self):
        """ Returns the list of processes that have yet to be processed or ready. """
        return list(filter(lambda p : not (p.is_marked_completed or self.is_queued(p) or p == self._processor.current_process), self._processes))

    def enqueue(self, *processes: Process):
        """ Adds processes to the ready queue. """
        self._ready_queue.extend(processes)
    
    def is_queued(self, process: Process):
        """ Checks whether a given queue is already ready to be processed. """
        return process in self._ready_queue

    def get_arrived_processes(self, timestamp: int):
        """ Gets all the arrived processes from the waiting queue based on a given timestamp. """
        return list(filter(lambda p : p.arrival <= timestamp, self.waiting_queue))
    

    @abstractmethod
    def run(self, timestamp: int, preempt: bool = True) -> List[Process]:
        """ Runs the scheduler at a given timestamp to process the ready queue. """
        pass