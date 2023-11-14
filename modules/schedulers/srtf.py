from .scheduler import Scheduler

class SRTF(Scheduler):
    name = "Shortest Remaining Time First (SRTF)"

    def process_queue(self, timestamp: int, preempt: bool = True):
        arrived_processes = self.get_arrived_processes(timestamp)

        if len(arrived_processes) > 0:
            if preempt and self._processor.is_occupied and not self._processor.is_finished:
                process = self._processor.clear()
                self.ready_queue.append(process)

            self.ready_queue.extend(arrived_processes)
            self.ready_queue.sort(key=lambda p : (p.burst_remaining, p.arrival, p.pid))
        
        return self.ready_queue