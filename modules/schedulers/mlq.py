from typing import List, Callable

from models import Process
from modules import Processor
from modules.schedulers import Scheduler, FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF

class MLQ(Scheduler):
    name: str = "Multilevel Queue (MLQ)"
    has_queue_level_field: bool = True
    is_multilevel: bool = True

    def __init__(self, processes: List[Process], processor: Processor, layers: List[Callable[[List[Process], Processor], Scheduler]]):
        super().__init__(processes, processor)
        self.__layers: List[Scheduler] = []

        for ql in range(len(layers)):
            ql_processes = list(filter(lambda p : p.queue_level == ql, processes))
            layer = layers[ql](ql_processes, processor)
            
            if isinstance(layer, RoundRobin):
                # Ensures that when two or more round robins exists, only the running round robin is ticking its time window
                # The l = layer is a workaround to keep the layer block scoped, as layer is local scoped 
                self._processor.on_clear(lambda _, l = layer : self._processor.off_tick(l.decrement_time_window))

            self.__layers.append(layer)

    @staticmethod
    def layer_choices() -> List[Scheduler]:
        return [FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF]
    
    @classmethod
    def create(cls, layers: List[Callable[[List[Process], Processor], Scheduler]]):
        """ A method that returns a partially instantiated scheduler that can be latched onto the operating system for use. """
        partialized_instance: Callable[[List[Process], Processor], cls] = lambda pl, p : cls(pl, p, layers)
        return partialized_instance

    def is_queued(self, process: Process):
        return any(map(lambda layer : process in layer._ready_queue, self.__layers))

    def run(self, timestamp: int, is_allowed_to_preempt: bool = True) -> List[Process]:
        current_layer = self.__layers[self._processor.current_process.queue_level] if self._processor.is_occupied else None
        arrived_processes = self.get_arrived_processes(timestamp)

        # Preempt on the arrival of a higher queue level process
        if len(arrived_processes) > 0 and self._processor.is_occupied:
            process_with_lowest_queue_level = min(list(map(lambda p : p.queue_level, arrived_processes)))
            higher_queue_level_process_arrived = self._processor.current_process.queue_level > process_with_lowest_queue_level 
        
            if is_allowed_to_preempt and higher_queue_level_process_arrived and self._processor.is_occupied and not self._processor.is_finished:
                preempted_process = self._processor.clear()
                
                # Preserve the time window if the round robin was not able to fully allow a process to completely run
                if isinstance(current_layer, RoundRobin) and not current_layer.is_time_window_consumed:
                    current_layer.requeue(preempted_process)
                
                current_layer = None

        # Let the sub-schedulers do their own thing
        for layer in self.__layers:
            layer.run(timestamp, is_allowed_to_preempt=layer == current_layer) 

        # Get topmost layer's ready queue
        if self._processor.is_idle:
            for layer in self.__layers:
                if len(layer._ready_queue) > 0:
                    self._ready_queue = layer._ready_queue
                    if isinstance(layer, RoundRobin):
                        self._processor.on_tick(layer.decrement_time_window)
                    break 

        return self._ready_queue