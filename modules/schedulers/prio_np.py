from .scheduler import Scheduler

class PriorityNP(Scheduler):
    @staticmethod
    def name():
        return "Priority Non-Preemptive (Prio-NP)"
    
    @staticmethod
    def is_priority_required():
        return True

    def process_queue(self, timestamp: int, _: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)

            if len(arrived_processes) > 0:
                self._ready_queue.extend(arrived_processes)
                self._ready_queue.sort(key=lambda p : (p.priority, p.burst, p.arrival, p.pid))
        return self._ready_queue