from typing import Optional, Callable, List

from utils.signal import Signal
from models import Clock, Process, ProcessLog

class Processor:
    def __init__(self, clock: Clock):
        self.__clock = clock
        self.__start_time: int = 0
        
        self.__idle_time: int = 0
        self.__current_process: Optional[Process] = None
        self.__process_logs: List[ProcessLog] = []

        self.__tick_signal = Signal[Process]()
        self.__clear_signal = Signal[Process]()
        self.__process_add_signal = Signal[Process]()

        self.__clear_signal.listen(self.__record_cleared_process)
        self.__process_add_signal.listen(self.__record_idle_time)

    @property
    def __last_log_end_time(self):
        """ Retrieves the end time of the last item in the execution timeline."""
        return self.__process_logs[-1].end if len(self.__process_logs) > 0 else self.__start_time

    def __record_cleared_process(self, cleared_process: Process):
        """ Records the cleared process to the logs. """
        log = ProcessLog(cleared_process.pid, self.__last_log_end_time, self.__clock.time, tag=cleared_process.queue_level)
        self.__process_logs.append(log)

    def __record_idle_time(self, loaded_process: Process):
        """ Records the idle time to the execution timeline. """
        if self.__last_log_end_time < self.__clock.time:
            self.__idle_time += self.__clock.time - self.__last_log_end_time
            
            log = ProcessLog("idle", self.__last_log_end_time, self.__clock.time, tag=loaded_process.queue_level)
            self.__process_logs.append(log)
    
    @property
    def is_idle(self):
        return self.__current_process is None
    
    @property
    def is_occupied(self):
        return self.__current_process is not None
    
    @property
    def is_finished(self):
        return self.is_occupied and self.__current_process.is_depleted
    
    @property
    def idle_time(self):
        return self.__idle_time
    
    @property
    def process_dump(self):
        """ Retrieve the logs of the processes that were processed by the processor. """
        return self.__process_logs

    @property
    def current_process(self):
        return self.__current_process
    
    def run(self, time_quantum = 1):
        """ Runs the processor by a given time quantum. """
        if self.is_occupied:
            for _ in range(time_quantum):
                if not self.__current_process.is_depleted:
                    self.__current_process.tick()
                    self.__tick_signal.emit(self.__current_process)
    
    def on_tick(self, fn: Callable[[Process], None]):
        """ Adds a function to listen whenever the processor does a tick. """
        self.__tick_signal.listen(fn)
    
    def off_tick(self, fn: Callable[[Process], None]):
        """ Removes a function listening to the processor tick. """
        self.__tick_signal.ignore(fn)

    def load(self, process: Process):
        """ Loads a process onto the processor for processing. """ 
        self.__current_process = process
        self.__process_add_signal.emit(self.__current_process)

    def on_load(self, fn: Callable[[Process], None]):
        """ Adds a function to listen whenever the processor loads a process. """
        self.__process_add_signal.listen(fn)
    
    def off_load(self, fn: Callable[[Process], None]):
        """ Removes a function listening to the processor load. """
        self.__process_add_signal.ignore(fn)

    def clear(self):
        """ Removes a loaded process from the processor, and returns that removed process to the caller. """
        cleared_process = None
        
        if self.is_occupied:
            cleared_process = self.__current_process
            self.__current_process = None
            self.__clear_signal.emit(cleared_process)

        return cleared_process 

    def on_clear(self, fn: Callable[[Process], None]):
        """ Adds a function to listen whenever the processor clears itself of a running process. """
        self.__clear_signal.listen(fn)
    
    def off_clear(self, fn: Callable[[Process], None]):
        """ Removes a function listening to the processor clear. """
        self.__clear_signal.ignore(fn)