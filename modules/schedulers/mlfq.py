from typing import List, Callable, Optional

from models import Process
from modules import Processor
from modules.schedulers import Scheduler, FCFS, SJF, PriorityNP, RoundRobin

class MLFQ(Scheduler):
    name: str = "Multilevel Feedback Queue (MLFQ)"

    def __init__(self, processes: List[Process], processor: Processor, time_quantums: List[int], last_layer: Callable[[List[Process], Processor], Scheduler]):
        super().__init__(processes, processor)
        self.__layers: List[Scheduler] = []
        self.__process_queue_levels: dict[int, Optional[int]] = { p.pid: None for p in processes }

        # Initialize the layers
        for idx in range(len(time_quantums)):
            rr_instance = RoundRobin.create(time_quantums[idx], False)
            layer = rr_instance(processes if idx == 0 else [], processor)
            
            # Ensures that only the running round robin is ticking its time window
            # The l = layer is a workaround to keep the layer block scoped, as layer is local scoped 
            self._processor.on_clear(lambda _, l = layer : self._processor.off_tick(l.decrement_time_window))
            self.__layers.append(layer)
        
        self.__layers.append(last_layer(processes, processor)) 

    @staticmethod
    def allowed_last_layer_scheduler() -> List[Scheduler]:
        return [FCFS, SJF, PriorityNP]
    
    @classmethod
    def create(cls, time_quantums: List[int], last_layer: Callable[[List[Process], Processor], Scheduler]):
        """ A method that returns a partially instantiated scheduler that can be latched onto the operating system for use. """
        partialized_instance: Callable[[List[Process], Processor], cls] = lambda pl, p : cls(pl, p, time_quantums, last_layer)
        return partialized_instance

    @property
    def round_robin_layers(self) -> List[RoundRobin]:
        return self.__layers[:-1]
    
    @property
    def last_layer(self):
        return self.__layers[-1]

    @property
    def previous_process(self):
        prev_process = None
        for layer in self.round_robin_layers:
            if layer.has_previous_process:
                prev_process = layer.previous_process
                break

        return prev_process
    
    def is_queued(self, process: Process):
        return self.__process_queue_levels[process.pid] is not None

    def process_queue(self, timestamp: int, _: bool = True) -> List[Process]:
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)
                
            if len(arrived_processes) > 0:
                arrived_processes.sort(key=lambda p : (p.arrival, p.pid))
                self.round_robin_layers[0].ready_queue.extend(arrived_processes)
                    
                for p in arrived_processes:
                    self.__process_queue_levels[p.pid] = 0

            if self.previous_process is not None:
                pid = self.previous_process.pid

                if self.__process_queue_levels[pid] < len(self.round_robin_layers):
                    current_layer = self.round_robin_layers[self.__process_queue_levels[pid]]
                    self.__process_queue_levels[pid] += 1
                
                    if self.__process_queue_levels[pid] < len(self.round_robin_layers):
                        next_layer = self.round_robin_layers[self.__process_queue_levels[pid]]
                        next_layer.ready_queue.append(self.previous_process) 

                current_layer.previous_process = None
            
            for rr_layer in self.round_robin_layers:
                if len(rr_layer.ready_queue) > 0:
                    self._processor.on_tick(rr_layer.decrement_time_window)
                    self._ready_queue = rr_layer.ready_queue
                    break
            
            if len(self._ready_queue) == 0:
                self.last_layer.process_queue(timestamp, False)
                self._ready_queue = self.last_layer.ready_queue

        return self._ready_queue