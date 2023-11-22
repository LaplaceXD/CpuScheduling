from models import Process
from .scheduler import Scheduler

class PriorityNP(Scheduler):
    name: str = "Priority Non-Preemptive (Prio-NP)"
    is_priority_required: bool = True

    def enqueue(self, *processes: Process):
        self._ready_queue.extend(processes)
        self._ready_queue.sort(key=lambda p : (p.priority, p.burst, p.arrival, p.pid))
    
    def run(self, timestamp: int, preempt: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)
        
            if len(arrived_processes) > 0:
                self.enqueue(*arrived_processes)

        return self._ready_queue