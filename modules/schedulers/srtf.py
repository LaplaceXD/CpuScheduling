from .scheduler import Scheduler

class SRTF(Scheduler):
    @staticmethod
    def name():
        return "Shortest Remaining Time First (SRTF)"

    def process_queue(self, timestamp: int, preempt: bool = True):
        arrived_processes = self.get_arrived_processes(timestamp)

        if len(arrived_processes) > 0:
            if preempt and self._processor.is_occupied and not self._processor.is_finished:
                process = self._processor.clear()
                self._ready_queue.append(process)

            self._ready_queue.extend(arrived_processes)
            self._ready_queue.sort(key=lambda p : (p.burst_remaining, p.arrival, p.pid))
        
        return self._ready_queue