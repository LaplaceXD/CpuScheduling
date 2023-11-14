from typing import Callable, List, Optional

from .scheduler import Scheduler
from models import Process
from modules import Processor

class RoundRobin(Scheduler):
    name = "Round Robin (RR)"

    def __init__(self, processes: List[Process], processor: Processor, time_quantum: int, is_decrement_automatic: bool = True):
        super().__init__(processes, processor)
        self.__time_quantum: int = time_quantum
        self.__time_window: int = time_quantum
        self.__previous_process: Optional[Process] = None

        self._processor.on_clear(self.__reset_time_window)

        if is_decrement_automatic:
            self._processor.on_tick(self.decrement_time_window)
    
    @classmethod
    def create(cls, time_quantum: int, is_decrement_automatic: bool = True):
        """ A method that returns a partially instantiated scheduler that can be latched onto the operating system for use. """
        partialized_instance: Callable[[List[Process, Processor], cls]] = lambda pl, p : cls(pl, p, time_quantum, is_decrement_automatic)
        return partialized_instance

    @property
    def time_quantum(self):
        return self.__time_quantum

    @property
    def previous_process(self):
        return self.__previous_process
    
    @property
    def has_previous_process(self):
        return self.__previous_process is not None
    
    def clear_previous_process(self):
        """ Clears the previous process of the scheduler. """
        self.__previous_process = None

    def __reset_time_window(self, _: Process):
        """ Resets the time window to the original time quantum value. """
        self.__time_window = self.__time_quantum 

    def decrement_time_window(self, current_process: Process):
        """ Decrements the time window as long as there is a process being processed. """
        self.__time_window -= 1
        if self.__time_window == 0 and not current_process.is_depleted:
            self.__previous_process = self._processor.clear()
    
    def process_queue(self, timestamp: int, _: bool = True) -> List[Process]:
        if self.__time_window == self.__time_quantum:
            arrived_processes = list(filter(lambda p : p != self.__previous_process, self.get_arrived_processes(timestamp)))

            if len(arrived_processes) > 0:
                arrived_processes.sort(key=lambda p : (p.arrival, p.pid))
                self.ready_queue.extend(arrived_processes)

            if self.has_previous_process:
                self.ready_queue.append(self.__previous_process)
                self.clear_previous_process()

        return self.ready_queue