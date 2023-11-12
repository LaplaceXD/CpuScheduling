# ===========================================================
# Authors:  Jonh Alexis Buot
#           Vladymir Godornes Roman
# Date:     November 11, 2023
# Course:   CS 3104 - Operating Systems
# Activity: CPU Scheduling Algorithm: Shortest Job First
# ===========================================================

import os

# ==== UTIL FUNCTIONS =====
def find(pred, iterable):
    for elem in iterable:
        if pred(elem):
            return elem
    return None

def trynuminput(prompt, min = 1):
    result = None
    while result is None:
        try:
            result = int(input(prompt))
            if(result < min):
                result = None
                raise ValueError()
        except KeyboardInterrupt:
            exit(1)
        except:
            print("The input should be a number that is at least equal to {}.".format(min))
    return result
# ==== UTIL FUNCTIONS =====

# ===== PROCESS DEFINITIONS =====
def sequence(start = 1):
    value = start

    while True:
        yield value
        value += 1

class Process:
    id_seq = sequence()
    
    def __init__(self, pid, arrival_time, burst_time, priority = 1):
        # Change this depending on requirements
        self._pid = pid
        self._arrival = arrival_time
        self._burst = burst_time
        self._priority = priority

        self._burst_remaining = burst_time
        self._completion = -1
        self._turnaround = -1
        self._waiting = -1
    
    @property 
    def pid(self):
        return self._pid
    
    @property 
    def priority(self):
        return self._priority
    
    @property 
    def arrival(self):
        return self._arrival
    
    @property 
    def burst(self):
        return self._burst
 
    @property
    def burst_remaining(self):
        return self._burst_remaining
    
    @property 
    def completion(self):
        return self._completion
    
    @property 
    def turnaround(self):
        return self._turnaround
    
    @property 
    def waiting(self):
        return self._waiting
    
    @property
    def is_completed(self):
        return self._completion != -1
    
    @property
    def is_pending(self):
        return self._completion == -1

    def tick(self, time = 1):
        self._burst_remaining -= time

    def end(self, timestamp):
        self._completion = timestamp
        self._turnaround = self._completion - self._arrival
        self._waiting = self._turnaround - self._burst

    @staticmethod
    def prompt():
        pid = next(Process.id_seq)

        print("===== P" + str(pid) + " Details =====")
        arrival_time = trynuminput("Arrival Time: ") 
        burst_time = trynuminput("Burst Time: ") 
       
        return Process(pid, arrival_time, burst_time)
# ===== PROCESS DEFINITIONS =====

# ===== SCHEDULER DEFINITIONS =====
class ExecutionRecord:
    def __init__(self, pid, start_time, completion_time):
        self._pid = pid
        self._start = start_time
        self._end = completion_time

    @property
    def pid(self):
        return self._pid
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    @property
    def duration(self):
        return self._end - self._start

class ExecutionTrail:
    def __init__(self):
        self._trail = []

    @property
    def trail(self):
        return self._trail

    @property
    def last_recorded_completion(self):
        return 0 if len(self._trail) == 0 else self._trail[-1].end

    def add_trail(self, name, end_time):
        record = ExecutionRecord(name, self.last_recorded_completion, end_time)
        self._trail.append(record)

class Processor:
    def __init__(self):
        self._running_process = None
        self._has_ran = False
        self._on_process_tick_subs = []

    @property
    def is_occupied(self):
        return self._running_process is not None
    
    @property
    def is_idle(self):
        return self._running_process is None
    
    @property
    def is_completed(self):
        return self.is_occupied and self._running_process.burst_remaining == 0

    @property
    def has_ran(self):
        return self._has_ran

    @property
    def running_process(self):
        return self._running_process
    
    def on_process_tick(self, fn):
        self._on_process_tick_subs.append(fn)
    
    def process(self, process):
        self._running_process = process

    def clear(self):
        self._running_process = None
        self._has_ran = False

    def tick(self, time = 1):
        if self.is_occupied:
            self._running_process.tick(time)
            self._has_ran = True
            for fn in self._on_process_tick_subs:
                fn(self._running_process.burst_remaining)

class Scheduler:
    def __init__(self, processes = [], processor = None):
        self.processes = processes
        self.processor = processor
        self.ready_queue = []

    def tick(self, time):
        return self.ready_queue

class OS:
    def __init__(self, scheduler, processes = []):
        self._processes = processes
        self._processor = Processor()
        self._trail = ExecutionTrail()
        self._scheduler = scheduler(self._processes, self._processor)

        self._running_time = -1     # -1 means not started

    @property
    def running_time(self):
        return self._running_time

    @property
    def idle_time(self):
        idle = filter(lambda e : e.pid == "idle", self._trail.trail)
        
        total = 0
        for i in idle:
            total += i.duration
        return total

    @property
    def total_turnaround_time(self):
        total = 0
        for p in self._processes:
           total += p.turnaround
        return total
    
    @property
    def total_waiting_time(self):
        total = 0
        for p in self._processes:
           total += p.waiting
        return total

    @property
    def execution_trail(self):
        return self._trail.trail

    def run(self):
        while any(map(lambda p : p.is_pending, self._processes)):
            self._running_time += 1
            ready_queue = self._scheduler.tick(self._running_time)

            if self._processor.is_occupied:
                self._processor.tick()
                
                if self._processor.is_completed:
                    self._trail.add_trail(self._processor.running_process.pid, self._running_time)
                    self._processor.running_process.end(self._running_time)
                    self._processor.clear()
                    ready_queue = self._scheduler.tick(self._running_time)
            
            if len(ready_queue) > 0 and self._processor.is_idle:
                process = ready_queue.pop(0)
                self._processor.process(process)
            
            if self._processor.is_occupied and not self._processor.has_ran and self._trail.last_recorded_completion < self._running_time:
                self._trail.add_trail("idle", self._running_time)
# ===== SCHEDULER DEFINITIONS =====

# ===== RENDERER DEFINITIONS =====
class Renderer:
    def __init__(self, cell_size):
        self.cell_size = cell_size

    def format_cell(self, cell):
        return "{:>{}}".format(cell, self.cell_size)

    def format_row(self, items, sep = "|"):
        row = ""
        row += sep
        row += sep.join([self.format_cell(i) for i in items]) 
        row += sep

        return row 

class Table(Renderer):
    def __init__(self, cell_size = 5, headers = []):
        super().__init__(cell_size)
        self.data = []
        self.headers = headers

    def add_data(self, *data):
        self.data.append(data)
        return self

    def __str__(self):
        table = ""
        bar_line = "+" + "-" * ((self.cell_size + 1) * len(self.headers) - 1) + "+\n"
        
        # Top Bar Line
        table += bar_line
        table += self.format_row(self.headers) + "\n"
        table += bar_line

        for data in self.data:
            table += self.format_row(data) + "\n"
        table += bar_line
    
        return table

class Gantt(Renderer):
    def __init__(self, cell_size=4):
        super().__init__(cell_size)
        self.headers = []
        self.timestamps = []

    def add_data(self, name, time):
        self.headers.append(name)
        self.timestamps.append(time)
        return self
    
    def __str__(self):
        gantt = ""
        bar_line = ("+" + "-" * self.cell_size) * len(self.headers) + "+\n"

        gantt += bar_line
        gantt += self.format_row(self.headers) + "\n"
        gantt += bar_line
        gantt += "0" + self.format_row(self.timestamps, sep=" ")

        return gantt
# ===== RENDERER DEFINITIONS =====

# ===== LOGIC STARTS HERE =====
class SJF(Scheduler):
    def tick(self, time):
        if self.processor.is_idle:
            arrived_processes = list(filter(lambda p : p.arrival <= time and p.is_pending and p not in self.ready_queue, self.processes))
            arrived_processes.sort(key=lambda p : (p.burst, p.pid))
            self.ready_queue.extend(arrived_processes)
        return self.ready_queue

def main():
    process_list = []

    print("Shortest Job First - Simulator")
    processes = trynuminput("Number of processes: ")

    for _ in range(processes):
        os.system("cls")
        process = Process.prompt() 
        process_list.append(process)

    oss = OS(SJF, process_list)
    oss.run()

    # ===== METRICS SUMMARY =====
    os.system("cls")
    print("===== SHORTEST JOB FIRST (SJF) - CPU SCHEDULING =====")
    print("# PROCESS TABLE")
    summary = Table(headers=["PID", "AT", "BT", "CT", "TAT", "WT"])
    for p in process_list:
        summary.add_data(p.pid, p.arrival, p.burst, p.completion, p.turnaround, p.waiting)
    print(summary)

    print("# GANTT CHART - TIMELINE")
    gantt = Gantt()
    for trail in oss.execution_trail:
        gantt.add_data("P" + str(trail.pid) if type(trail.pid) == int else trail.pid, trail.end)
    print(gantt)

    print("\n# METRICS")
    print("CPU Utilization: {:.2f}%".format(((oss.running_time - oss.idle_time) / oss.running_time) * 100))
    print("Average TAT: {:.2f}".format(oss.total_turnaround_time / len(process_list)))
    print("Average WT: {:.2f}".format(oss.total_waiting_time / len(process_list)))
# ===== LOGIC ENDS HERE =====

if __name__ == "__main__":
    main()