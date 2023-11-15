import os
from typing import List, Optional

from modules import OS
from modules.schedulers import Scheduler, FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF, MLQ, MLFQ
from models import Process
from views import Table, Gantt
from utils.io import input_bounded_num

def format_choice_list(choices: List[str]):
    return "\n".join(["[{}] {}".format(idx + 1, choices[idx]) for idx in range(len(choices))])

def print_metrics(oss: OS, with_prio: bool = False, with_queue_level: bool = False):
    table_headers: List[str] = ["PID", "AT", "BT", "CT", "TAT", "WT"] 
    if with_prio:
        # Insert at the index before CT
        idx = len(table_headers) - 3 
        table_headers.insert(idx, "Prio")
    
    if with_queue_level:
        # Insert at the index before CT
        idx = len(table_headers) - 3 
        table_headers.insert(idx, "QL")

    table: Table = Table(headers=table_headers)
    
    for p in oss.processes:
        data = ["P" + str(p.pid), p.arrival, p.burst, p.completion, p.turnaround, p.waiting]
        if with_prio:
            # Insert at the index before completion time
            idx = len(data) - 3 
            data.insert(idx, p.priority)
    
        if with_queue_level:
            # Insert at the index before completion time
            idx = len(data) - 3 
            data.insert(idx, p.queue_level + 1)

        table.add_data(*data)
    
    gantt: Gantt = Gantt()
    for trail in oss.execution_trail:
        gantt.add_data("P" + str(trail.name) if type(trail.name) == int else trail.name, trail.end)
    
    print("# PROCESS TABLE")
    table.render()

    print("# GANTT CHART - TIMELINE")
    gantt.render()
    print()

    print("# METRICS")
    print("CPU Utilization: {:.2f}%".format((float(oss.running_time - oss.idle_time) / float(oss.running_time)) * 100))
    print("Average TAT: {:.2f}".format(sum(p.turnaround for p in oss.processes) / len(oss.processes)))
    print("Average WT: {:.2f}".format(sum(p.waiting for p in oss.processes) / len(oss.processes)))    

def configure_round_robin(is_decrement_automatic: bool):
    time_quantum = input_bounded_num("Time quantum: ") 
    return RoundRobin.create(time_quantum, is_decrement_automatic)

def configure_mlq(num_layers: int):
    with_prio, mlq_layers, mlq_layer_names = (False, [], [])
    layer_choices = MLQ.allowed_schedulers()
    print(format_choice_list(list(map(lambda s : s.name, layer_choices))))
    for layer_num in range(num_layers):
        scheduler_choice = input_bounded_num("Layer #{}: ".format(layer_num + 1), max=len(layer_choices))

        layer_scheduler = layer_choices[scheduler_choice - 1]
        if layer_scheduler == RoundRobin:
            time_quantum = input_bounded_num("Time quantum: ") 
            mlq_layer_names.append(layer_scheduler.name + " | q=" + str(time_quantum))
            mlq_layers.append(layer_scheduler.create(time_quantum, False))
        else:
            mlq_layer_names.append(layer_scheduler.name)
            mlq_layers.append(layer_scheduler.create())

        if layer_scheduler.is_priority_required:
            with_prio = True

    mlq_config = format_choice_list(mlq_layer_names)
    return (MLQ.create(mlq_layers), mlq_config, with_prio)

def configure_mlfq(num_layers: int):
    allowed_last_layers = MLFQ.allowed_last_layer_scheduler()
    layer_names = []
    time_quantums = []

    for i in range(num_layers - 1):
        layer_time_quantum = input_bounded_num("RR #{} - Time Quantum: ".format(i + 1))
        time_quantums.append(layer_time_quantum)
        layer_names.append(RoundRobin.name + " | q=" + str(layer_time_quantum))

    print()
    print(format_choice_list(list(map(lambda s : s.name, allowed_last_layers))), end="\n\n")
    selected_end_layer = input_bounded_num("Select End Layer: ", max=len(allowed_last_layers))
    
    end_layer = allowed_last_layers[selected_end_layer - 1]
    layer_names.append(end_layer.name)
    with_prio = end_layer.is_priority_required

    mlfq_config = format_choice_list(layer_names)
    return (MLFQ.create(time_quantums, end_layer.create()), mlfq_config, with_prio)

def main():
    process_list: List[Process] = []
    scheduler_choices: List[Scheduler] = [FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF, MLQ, MLFQ] 
    
    print("===== CPU Scheduling Simulator =====")
    print(format_choice_list(list(map(lambda s : s.name, scheduler_choices))), end="\n\n")
    scheduler_choice = input_bounded_num("Select a scheduler: ", max=len(scheduler_choices))

    scheduler: Scheduler = scheduler_choices[scheduler_choice - 1]
    with_prio: bool = scheduler.is_priority_required
    with_queue_level: bool = scheduler.is_queue_level_required

    time_quantum = 0
    mlq_config = None
    mlfq_config = None
    scheduler_instance: Optional[Scheduler] = None
    if scheduler == RoundRobin:
        print("\n=====", scheduler.name, "Configuration =====")
        time_quantum = input_bounded_num("Time quantum: ") 
        scheduler_instance = scheduler.create(time_quantum, True)
        print()
    elif scheduler == MLQ:
        print("\n=====", scheduler.name, "Configuration =====")
        num_layers = input_bounded_num("Number of Layers: ")
        scheduler_instance, mlq_config, with_prio = configure_mlq(num_layers)
        print()
    elif scheduler == MLFQ:
        print("\n=====", scheduler.name, "Configuration =====")
        num_layers = input_bounded_num("Number of Layers: ")
        scheduler_instance, mlfq_config, with_prio = configure_mlfq(num_layers)
        print()
    else:
        scheduler_instance = scheduler.create()

    num_of_processes = input_bounded_num("Number of processes: ")
    for _ in range(num_of_processes):
        os.system("cls")
        pid = next(Process.id_sequence)

        print("===== P" + str(pid) + " Details =====")
        if with_queue_level:
            print(mlq_config, end="\n\n")
        
        arrival_time = input_bounded_num("Arrival Time: ", 0) 
        burst_time = input_bounded_num("Burst Time: ")
        priority = input_bounded_num("Priority: ") if with_prio else 1
        queue_level = input_bounded_num("Queue Level: ") if with_queue_level else 1

        process = Process(pid, arrival_time, burst_time, priority, queue_level - 1)
        process_list.append(process)

    oss = OS(scheduler_instance, process_list)
    oss.run()

    os.system("cls")
    print("===== CPU Scheduling Simulator =====")
    print("Scheduler: ", scheduler.name, " | q=" + str(time_quantum) if scheduler is RoundRobin else "")
    if scheduler == MLQ:
        print()
        print("# LAYER CONFIGURATION")
        print(mlq_config)
    elif scheduler == MLFQ:
        print()
        print("# LAYER CONFIGURATION")
        print(mlfq_config)

    print()
    print_metrics(oss, with_prio, with_queue_level)
    
if __name__ == "__main__":
    main()