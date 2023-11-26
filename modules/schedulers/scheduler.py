from typing import List, Callable
from abc import ABC, abstractmethod

from models import Process
from ..processor import Processor

class Scheduler(ABC):
    name: str = "Scheduler"
    has_priority_field: bool = False
    has_queue_level_field: bool = False
    is_multilevel: bool = False

    def __init__(self, processes: List[Process], processor: Processor):
        self._processes: List[Process] = processes
        self._processor: Processor = processor
        self._ready_queue: List[Process] = []

    def __str__(self):
        return self.name
    
    @classmethod
    def factory(cls):
        """ 
            A factory for schedulers that has some of their unique properties 
            (e.g. time quantum, layers) partially initialized. This ensures that
            when working with other schedulers only process_list and processor are
            required, while still being able to initialize the scheduler with other
            useful properties.
        """
        factory: Callable[[List[Process], Processor], cls] = lambda pl, p : cls(pl, p)
        return factory

    @property
    def waiting_queue(self):
        """ Returns the list of processes that have yet to be processed or ready. """
        return [p for p in self._processes if not (p.is_marked_completed or self.is_queued(p) or p == self._processor.current_process)]

    def enqueue(self, *processes: Process):
        """ Adds processes to the ready queue. """
        self._ready_queue.extend(processes)
    
    def is_queued(self, process: Process):
        """ Checks whether a given queue is already ready to be processed. """
        return process in self._ready_queue

    def get_arrived_processes(self, timestamp: int):
        """ Gets all the arrived processes from the waiting queue based on a given timestamp. """
        return [p for p in self.waiting_queue if p.arrival <= timestamp]
    
    @abstractmethod
    def run(self, timestamp: int, is_allowed_to_preempt: bool = True) -> List[Process]:
        """ Runs the scheduler at a given timestamp to process the ready queue. """
        pass