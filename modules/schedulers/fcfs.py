from models import Process
from .scheduler import Scheduler 

class FCFS(Scheduler):
    name: str = "First Come First Serve (FCFS)"
    
    def enqueue(self, *processes: Process):
        self._ready_queue.extend(processes)
        self._ready_queue.sort(key=lambda p : (p.arrival, p.pid))

    def run(self, timestamp: int, is_allowed_to_preempt: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)
        
            if len(arrived_processes) > 0:
                self.enqueue(*arrived_processes)

        return self._ready_queue