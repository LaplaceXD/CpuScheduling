from typing import List, Callable

from models import Process
from modules import Processor
from modules.schedulers import Scheduler, FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF

class MLQ(Scheduler):
    name: str = "Multilevel Queue (MLQ)"
    is_queue_level_required: bool = True

    def __init__(self, processes: List[Process], processor: Processor, layers: List[Callable[[List[Process], Processor], Scheduler]]):
        super().__init__(processes, processor)
        self.__layers: List[Scheduler] = []

        for ql in range(len(layers)):
            ql_processes = list(filter(lambda p : p.queue_level == ql, processes))
            layer = layers[ql](ql_processes, processor)
            
            if RoundRobin.is_instance(layer):
                # Ensures that when two or more round robins exists, only the running round robin is ticking its time window
                # The l = layer is a workaround to keep the layer block scoped, as layer is local scoped 
                self._processor.on_clear(lambda _, l = layer : self._processor.off_tick(l.decrement_time_window))

            self.__layers.append(layer)

    @staticmethod
    def allowed_schedulers() -> List[Scheduler]:
        return [FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF]
    
    @classmethod
    def create(cls, layers: List[Callable[[List[Process], Processor], Scheduler]]):
        """ A method that returns a partially instantiated scheduler that can be latched onto the operating system for use. """
        partialized_instance: Callable[[List[Process], Processor], cls] = lambda pl, p : cls(pl, p, layers)
        return partialized_instance

    def is_queued(self, process: Process):
        is_in_any_ready_queue = any(map(lambda layer : process in layer.ready_queue, self.__layers))
        is_previous_in_round_robin = any(map(lambda layer : RoundRobin.is_instance(layer) and process == layer.previous_process, self.__layers))

        return is_in_any_ready_queue or is_previous_in_round_robin

    def process_queue(self, timestamp: int, _: bool = True) -> List[Process]:
        current_layer = self.__layers[self._processor.current_process.queue_level] if self._processor.is_occupied else None
        arrived_processes = self.get_arrived_processes(timestamp)

        if len(arrived_processes) > 0:
            process_with_lowest_queue_level = min(list(map(lambda p : p.queue_level, arrived_processes)))
            preempt = self._processor.is_occupied and self._processor.current_process.queue_level > process_with_lowest_queue_level 
        
            if preempt and not self._processor.is_finished:
                preempted_process = self._processor.clear()

                if RoundRobin.is_instance(current_layer):
                    current_layer.previous_process = preempted_process
                else:
                    current_layer.ready_queue.append(preempted_process)

        for layer in self.__layers:
            layer.process_queue(timestamp, layer == current_layer) 

        if self._processor.is_idle:
            for layer in self.__layers:
                if len(layer.ready_queue) > 0:
                    self._ready_queue = layer.ready_queue
                    if RoundRobin.is_instance(layer):
                        self._processor.on_tick(layer.decrement_time_window)
                    break 

        return self._ready_queue