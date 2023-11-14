from .scheduler import Scheduler

class SJF(Scheduler):
    @staticmethod
    def name():
        return "Shortest Job First (SJF)"

    def process_queue(self, timestamp: int, _: bool = False):
        if self._processor.is_idle:
            arrived_processes = self.get_arrived_processes(timestamp)

            if len(arrived_processes) > 0:
                self._ready_queue.extend(arrived_processes)
                self._ready_queue.sort(key=lambda p: (p.burst, p.arrival, p.pid)) 
        return self._ready_queue