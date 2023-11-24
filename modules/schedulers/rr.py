from typing import Callable, List

from .scheduler import Scheduler
from models import Process
from modules import Processor

class RoundRobin(Scheduler):
    name: str = "Round Robin (RR)"

    def __init__(self, processes: List[Process], processor: Processor, time_quantum: int, is_decrement_automatic: bool = False):
        super().__init__(processes, processor)
        self.__time_quantum: int = time_quantum
        self.__time_window: int = time_quantum

        self._processor.on_load(self.__reset_time_window)

        if is_decrement_automatic:
            self._processor.on_tick(self.decrement_time_window)
    
    @classmethod
    def create(cls, time_quantum: int, is_decrement_automatic: bool = False):
        """ A method that returns a partially instantiated scheduler that can be latched onto the operating system for use. """
        partialized_instance: Callable[[List[Process], Processor], cls] = lambda pl, p : cls(pl, p, time_quantum, is_decrement_automatic)
        return partialized_instance

    @property
    def time_quantum(self):
        return self.__time_quantum

    def __reset_time_window(self, _: Process):
        """ Resets the time window to the original time quantum value. """
        self.__time_window = self.__time_quantum 

    def decrement_time_window(self, current_process: Process):
        """ Decrements the time window as long as there is a process being processed. """
        self.__time_window -= 1
        
        if self.__time_window == 0 and not current_process.is_depleted:
            self._processor.clear()
    
    def enqueue(self, *processes: Process):
        # The first sorting condition is just to make sure that previous processes are appended at the end
        self._ready_queue.extend(sorted(processes, key=lambda p : (0 if p.burst == p.burst_remaining else 1, p.arrival, p.pid)))
    
    def run(self, timestamp: int, is_allowed_to_preempt: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)
        
            if len(arrived_processes) > 0:
                self.enqueue(*arrived_processes)

        return self._ready_queue