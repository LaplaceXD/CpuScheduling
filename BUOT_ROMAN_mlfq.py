# ===========================================================
# Authors:  Jonh Alexis Buot
#           Vladymir Godornes Roman
# Date:     November 11, 2023
# Course:   CS 3104 - Operating Systems
# Activity: CPU Scheduling Algorithm: Multilayer Feedback Queue
# ===========================================================

from abc import ABC, abstractmethod
import os

# ==== UTIL FUNCTIONS =====
def find(pred, iterable):
    for elem in iterable:
        if pred(elem):
            return elem
    return None

def trynuminput(prompt, min = 1, max = None):
    result = None
    while result is None:
        try:
            result = int(input(prompt))
            if result < min or (max is not None and max < result):
                result = None
                raise ValueError()
        except KeyboardInterrupt:
            exit(1)
        except:
            if max is None:
                print("The input should be a number that is at least equal to {}.".format(min))
            else:
                print("The input should be a number between {} and {}.".format(min, max))
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
    def prompt(with_priority = False):
        pid = next(Process.id_seq)

        print("===== P" + str(pid) + " Details =====")
        arrival_time = trynuminput("Arrival Time: ", 0) 
        burst_time = trynuminput("Burst Time: ") 
        priority = trynuminput("Priority: ") if with_priority else 1

        return Process(pid, arrival_time, burst_time, priority)
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
        self._on_process_tick_subs = []
        self._on_clear_subs = []
        self._on_process_add_subs = []

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
    def running_process(self):
        return self._running_process
    
    def on_process_tick(self, fn):
        self._on_process_tick_subs.append(fn)
    
    def on_process_add(self, fn):
        self._on_process_add_subs.append(fn)
    
    def on_clear(self, fn):
        self._on_clear_subs.append(fn)
    
    def process(self, process):
        self._running_process = process
        for fn in self._on_process_add_subs:
            fn()

    def clear(self):
        for fn in self._on_clear_subs:
            fn()
        
        process = self._running_process
        self._running_process = None
        
        return process

    def tick(self, time = 1):
        if self.is_occupied:
            self._running_process.tick(time)
            
            for fn in self._on_process_tick_subs:
                fn(self._running_process.burst_remaining)

class Scheduler(ABC):
    def __init__(self, processes = [], processor = None):
        self.processes = processes
        self.processor = processor
        self.ready_queue = []
    
    @property
    def pending_queue(self):
        return list(filter(lambda p : p.is_pending and p not in self.ready_queue and p != self.processor.running_process, self.processes))

    @abstractmethod    
    def tick(self, time):
        pass

class OS:
    def __init__(self, scheduler, processes = []):
        self._running_time = -1     # -1 means not started
        self._idle_time = 0
        self._processes = processes
        self._trail = ExecutionTrail()

        self._processor = Processor()
        self._processor.on_clear(self.record_executed_process)
        self._processor.on_process_add(self.record_idle)
        
        self._scheduler = scheduler(self._processes, self._processor)

    def record_executed_process(self):
        if self._processor.is_occupied:
            self._trail.add_trail(self._processor.running_process.pid, self._running_time) 
    
    def record_idle(self):
        if self._processor.is_occupied and self._trail.last_recorded_completion < self.running_time:
            self._trail.add_trail("idle", self._running_time)
            self._idle_time += self._trail.trail[-1].duration 

    @property
    def running_time(self):
        return self._running_time

    @property
    def idle_time(self):
        return self._idle_time

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
  
            if self._processor.is_occupied:
                self._processor.tick()
                
                if self._processor.is_completed:
                    self._processor.running_process.end(self._running_time)
                    self._processor.clear()
  
            ready_queue = self._scheduler.tick(self._running_time)

            if len(ready_queue) > 0 and self._processor.is_idle:
                process = ready_queue.pop(0)
                self._processor.process(process)
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
def fcfs(queue):
    queue.sort(key=lambda p : (p.arrival, p.pid))

def sjf(queue):
    queue.sort(key=lambda p : (p.burst_remaining, p.arrival, p.pid))

def prionp(queue):
    queue.sort(key=lambda p : (p.priority,  p.burst_remaining, p.arrival, p.pid))

def MLFQFactory(rr_time_quantums = [], end_layer_sort = fcfs):
    class MLFQ(Scheduler):
        def __init__(self, processes = [], processor = None):
            super().__init__(processes, processor)
            self._time_quantums = rr_time_quantums
            self._previous_process = None
            self._process_levels = { p.pid: -1 for p in processes }
            self._time_allocation = 0 if len(rr_time_quantums) == 0 else rr_time_quantums[0]

            self.ready_queue = [[] for _ in range(len(self._time_quantums) + 1)]
            self.processor.on_process_tick(self.decrement_process_time_window)
            self.processor.on_process_add(self.set_time_allocation)
            
        @property
        def pending_queue(self):
            is_pending = lambda p : p.is_pending
            is_queued = lambda p : any(map(lambda rq : p in rq, self.ready_queue))
            is_running_process = lambda p : self.processor.running_process == p

            return list(filter(lambda p : is_pending(p) and not is_queued(p) and not is_running_process(p), self.processes))

        @property
        def current_quantum_time(self):            
            if self.processor.is_idle:
                return 0

            level = self._process_levels[self.processor.running_process.pid]
            return 0 if len(self._time_quantums) <= level else self._time_quantums[level]

        def decrement_process_time_window(self, remaining_time):
            self._time_allocation -= 1

            if self._time_allocation == 0 or remaining_time == 0: 
                self._time_allocation = self.current_quantum_time
                
                if remaining_time != 0:
                    self._previous_process = self.processor.clear()
        
        def set_time_allocation(self):
            self._time_allocation = self.current_quantum_time

        def tick(self, time):
            if self.processor.is_idle or self._time_quantums == self.current_quantum_time:
                if len(self.pending_queue) > 0:
                    arrived_processes = list(filter(lambda p : p.arrival <= time and p != self._previous_process, self.pending_queue))

                    if len(arrived_processes) > 0:
                        arrived_processes.sort(key=lambda p : (p.arrival, p.pid)) 
                        self.ready_queue[0].extend(arrived_processes)
                        for p in arrived_processes:
                            self._process_levels[p.pid] = 0

                if self._previous_process is not None:
                    self._process_levels[self._previous_process.pid] += 1
                    self.ready_queue[self._process_levels[self._previous_process.pid]].append(self._previous_process)
                    self._previous_process = None
            
            queue = []
            for rq in self.ready_queue[:-1]:
                if len(rq) > 0:
                    queue = rq
                    break

            # If queue remains 0, then we can delegate control to end_layer
            if len(queue) == 0:
                queue = self.ready_queue[-1]
                end_layer_sort(queue) 

            return queue
        
    return MLFQ

def main():
    process_list = [];

    print("Multilevel Feedback Queue - Simulator")
    processes = trynuminput("Number of processes: ")
   
    os.system("cls")
    print("===== MLFQ Configuration =====")
    round_robin_layers = trynuminput("Round Robin Layers: ")
    rr_time_quantums = []

    for i in range(round_robin_layers):
        tq = trynuminput("RR#{} Time Quantum: ".format(i + 1))
        rr_time_quantums.append(tq)

    print()
    print("[1] First Come First Serve (FCFS)")
    print("[2] Shortest Job First (SJF)")
    print("[3] Priority Non-Preemptive (Prio-NP)")
    end_layer_selected = trynuminput("Select End Layer: ", 1, 3) - 1
    end_layers = [fcfs, sjf, prionp]
    is_prio = end_layer_selected == 2 

    for _ in range(processes):
        os.system("cls")
        process = Process.prompt(with_priority=is_prio) 
        process_list.append(process)

    oss = OS(MLFQFactory(rr_time_quantums, end_layers[end_layer_selected]), process_list)
    oss.run()

    # ===== METRICS SUMMARY =====
    os.system("cls")
    print("===== MULTILEVEL FEEDBACK QUEUE (MLFQ) - CPU SCHEDULING =====")
    
    print("# PROCESS TABLE")
    headers = ["PID", "AT", "BT", "CT", "TAT", "WT"]
    if is_prio: headers.insert(3, "Prio")
    summary = Table(headers=headers)
    for p in process_list:
        data = [p.pid, p.arrival, p.burst, p.completion, p.turnaround, p.waiting]
        if is_prio: data.insert(3, p.priority)
        
        summary.add_data(*data)
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