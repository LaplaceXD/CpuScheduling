from typing import List

from models import Clock, Process
from .schedulers import Scheduler
from .processor import Processor

class Kernel:
    def __init__(self, scheduler: Scheduler, processes: List[Process]):
        self.__clock = Clock(start_time=-1) # -1 = not started
        
        self.__processes: List[Process] = processes
        self.__processor: Processor = Processor(clock=self.__clock)
        self.__scheduler: Scheduler = scheduler(self.__processes, self.__processor)
        
    @property
    def processes(self):
        return self.__processes

    @property
    def running_time(self):
        return self.__running_time

    @property
    def idle_time(self):
        return self.__processor.idle_time
    
    @property
    def execution_timeline(self):
        return self.__processor.process_dump

    def run(self):
        """ Runs the kernel to process the processes until all are completed. """ 
        while any(map(lambda p : not p.is_marked_completed, self.__processes)):
            self.__clock.tick()

            if self.__processor.is_occupied:
                self.__processor.run()
                
                if self.__processor.is_finished:
                    completed_process = self.__processor.clear()
                    completed_process.mark_completed_on(self.__clock.time) 
  
            ready_queue = self.__scheduler.run(self.__clock.time)

            if len(ready_queue) > 0 and self.__processor.is_idle:
                process = ready_queue.pop(0)
                self.__processor.load(process)