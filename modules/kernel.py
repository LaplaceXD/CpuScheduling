from typing import List

from models import Process, ExecutionFrame
from .schedulers import Scheduler
from .processor import Processor

class Kernel:
    def __init__(self, scheduler: Scheduler, processes: List[Process]):
        self.__running_time: int = -1                      # -1 = not started
        self.__start_time: int = 0
        self.__idle_time: int = 0
        self.__timeline: List[ExecutionFrame] = []
        
        self.__processes: List[Process] = processes
        self.__processor: Processor = Processor()
        self.__scheduler: Scheduler = scheduler(self.__processes, self.__processor)
        
        self.__processor.on_clear(self.__record_completed_process)
        self.__processor.on_load(self.__record_idle_time)

    @property
    def __last_timeline_execution_end_time(self):
        """ Retrieves the end time of the last item in the execution timeline."""
        return self.__timeline[-1].end if len(self.__timeline) > 0 else self.__start_time

    def __record_completed_process(self, completed_process: Process):
        """ Records the completed process to the execution timeline. """
        last_recorded_end_time = self.__last_timeline_execution_end_time

        frame = ExecutionFrame(completed_process.pid, last_recorded_end_time, self.__running_time, tag=completed_process.queue_level)
        self.__timeline.append(frame)

    def __record_idle_time(self, loaded_process: Process):
        """ Records the idle time to the execution timeline. """
        last_recorded_end_time = self.__last_timeline_execution_end_time

        if last_recorded_end_time < self.__running_time:
            self.__idle_time += self.__running_time - last_recorded_end_time
            
            frame = ExecutionFrame("idle", last_recorded_end_time, self.__running_time, tag=loaded_process.queue_level)
            self.__timeline.append(frame)

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
    def execution_timeline(self):
        return self.__timeline

    def run(self):
        """ Runs the kernel to process the processes until all are completed. """ 
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