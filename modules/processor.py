from typing import Optional, Callable
from utils.signal import Signal
from models.process import Process

class Processor:
    def __init__(self):
        self.__current_process: Optional[Process] = None
        
        self.__tick_signal = Signal[Process]()
        self.__clear_signal = Signal[Process]()
        self.__process_add_signal = Signal[Process]()

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