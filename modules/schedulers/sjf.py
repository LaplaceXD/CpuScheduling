from .scheduler import Scheduler

class SJF(Scheduler):
    name: str = "Shortest Job First (SJF)"

    def process_queue(self, timestamp: int, _: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)

            if len(arrived_processes) > 0:
                self.ready_queue.extend(arrived_processes)
                self.ready_queue.sort(key=lambda p: (p.burst, p.arrival, p.pid)) 
        return self.ready_queue