from typing import List
from abc import ABC, abstractmethod

from models import Process
from modules import Processor

class Scheduler(ABC):
    def __init__(self, processes: List[Process], processor: Processor):
        self._processes: List[Process] = processes
        self._processor: Processor = processor
        self._ready_queue: List[Process] = []
    
    @property
    def waiting_queue(self):
        """ Returns the list of processes that have yet to be processed or ready. """
        return list(filter(lambda p : not (p.is_marked_ended or self.is_queued(p) or p == self._processor.current_process), self._processes))

    def is_queued(self, process: Process):
        """ Checks whether a given queue is already ready to be processed. """
        return process in self._ready_queue

    def get_arrived_processes(self, timestamp: int):
        """ Gets all the arrived processes from the waiting queue based on a given timestamp. """
        return list(filter(lambda p : p.arrival <= timestamp, self.waiting_queue))

    @abstractmethod   
    def process_queue(self, timestamp: int, preempt: bool = True):
        """ Processes the ready queue. """
        pass