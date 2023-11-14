from .scheduler import Scheduler

class PriorityNP(Scheduler):
    name: str = "Priority Non-Preemptive (Prio-NP)"
    is_priority_required: bool = True

    def process_queue(self, timestamp: int, _: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)

            if len(arrived_processes) > 0:
                self._ready_queue.extend(arrived_processes)
                self._ready_queue.sort(key=lambda p : (p.priority, p.burst, p.arrival, p.pid))
        return self._ready_queue