from typing import List

from models import Process
from modules import ExecutionTrail, Processor
from modules.schedulers import Scheduler

class OS:
    def __init__(self, scheduler: Scheduler, processes: List[Process]):
        self.__running_time: int = -1       # -1 = not started
        self.__idle_time: int = 0
        self.__processes: List[Process] = processes
        
        self.__trail: ExecutionTrail = ExecutionTrail()
        self.__processor: Processor = Processor()
        self.__scheduler: Scheduler = scheduler(self.__processes, self.__processor)
        
        self.__processor.on_clear(self.__record_completed_process)
        self.__processor.on_load(self.__record_idle_time)

    def __record_completed_process(self, completed_process: Process):
        """ Records the completed process to the execution trail. """
        self.__trail.add_frame(completed_process.pid, self.__running_time) 

    def __record_idle_time(self, _: Process):
        """ Records the idle time to the execution trail. """
        if self.__trail.last_execution_end_time < self.__running_time:
            self.__idle_time += self.__running_time - self.__trail.last_execution_end_time 
            self.__trail.add_frame("idle", self.__running_time)

    @property
    def processes(self):
        return self.__processes

    @property
    def running_time(self):
        return self.__running_time

    @property
    def idle_time(self):
        return self.__idle_time
    
    @property
    def execution_trail(self):
        return self.__trail.trail

    def run(self):
        """ Runs the operating system. """ 
        while any(map(lambda p : not p.is_marked_completed, self.__processes)):
            self.__running_time += 1
  
            if self.__processor.is_occupied:
                self.__processor.run()
                
                if self.__processor.is_finished:
                    completed_process = self.__processor.clear()
                    completed_process.mark_completed_on(self.__running_time) 
  
            ready_queue = self.__scheduler.run(self.__running_time)

            if len(ready_queue) > 0 and self.__processor.is_idle:
                process = ready_queue.pop(0)
                self.__processor.load(process)