from ..models import Process
from .scheduler import Scheduler

class SRTF(Scheduler):
    name: str = "Shortest Remaining Time First (SRTF)"

    def enqueue(self, *processes: Process):
        self._ready_queue.extend(processes)
        self._ready_queue.sort(key=lambda p : (p.burst_remaining, p.arrival, p.pid))
    
    def run(self, timestamp: int, is_allowed_to_preempt: bool = True):
        arrived_processes = self.get_arrived_processes(timestamp)

        if len(arrived_processes) > 0:
            if is_allowed_to_preempt and self._processor.is_occupied and not self._processor.is_finished:
                process = self._processor.clear()
                arrived_processes.append(process)
            
            self.enqueue(*arrived_processes)
        
        return self._ready_queue