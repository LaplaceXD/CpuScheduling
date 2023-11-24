import os
from typing import List, Optional, Any

from modules import OS
from modules.schedulers import Scheduler, FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF, MLQ, MLFQ
from models import Process
from views import Table, Gantt
from utils.io import input_bounded_num

def format_choice_list(choices: List[str]):
    return "\n".join(["[{}] {}".format(idx + 1, choices[idx]) for idx in range(len(choices))])

def print_metrics(oss: OS, with_prio: bool = False, with_queue_level: bool = False, layers: List[str] = []):
    # Create the Table
    table_headers = ["PID", "AT", "BT", "CT", "TAT", "WT"] 
    if with_prio:
        # Insert at the index before CT
        idx = len(table_headers) - 3 
        table_headers.insert(idx, "Prio")
    
    if with_queue_level:
        # Insert at the index before CT
        idx = len(table_headers) - 3 
        table_headers.insert(idx, "QL")

    table = Table(headers=table_headers)
    
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
    
    layer_gantts: List[Gantt] = [Gantt(name="[{}]".format(i + 1), show_timestamps=i + 1 == len(layers)) for i in range(len(layers))]
    merged_gantt = Gantt(name="[A]" if len(layers) > 0 else None)
    for trail in oss.execution_trail:
        name = "P" + str(trail.name) if type(trail.name) == int else trail.name
        time = trail.end

        for tag, layer_gantt in enumerate(layer_gantts):
            layer_gantt.add_data(name if trail.tag == tag else "", time)

        merged_gantt.add_data(name, time)
    
    print("# PROCESS TABLE")
    table.render()

    print("# GANTT CHART - TIMELINE")
    if len(layer_gantts) > 0:
        for layer_gantt in layer_gantts:
            layer_gantt.render()
        print()

    merged_gantt.render()
    print()

    print("# METRICS")
    print("CPU Utilization: {:.2f}%".format((float(oss.running_time - oss.idle_time) / float(oss.running_time)) * 100))
    print("Average TAT: {:.2f}".format(sum(p.turnaround for p in oss.processes) / len(oss.processes)))
    print("Average WT: {:.2f}".format(sum(p.waiting for p in oss.processes) / len(oss.processes)))    

def configure_mlq(num_layers: int):
    with_prio = False
    layers = []
    layer_names = []
    layer_choices = MLQ.allowed_schedulers()
    
    print(format_choice_list(list(map(lambda s : s.name, layer_choices))))
    for layer_num in range(num_layers):
        scheduler_choice = input_bounded_num("Layer #{}: ".format(layer_num + 1), max=len(layer_choices))

        layer_scheduler = layer_choices[scheduler_choice - 1]
        if layer_scheduler == RoundRobin:
            time_quantum = input_bounded_num("Time quantum: ") 
            layer_names.append(layer_scheduler.name + " | q=" + str(time_quantum))
            layers.append(layer_scheduler.create(time_quantum, False))
        else:
            layer_names.append(layer_scheduler.name)
            layers.append(layer_scheduler.create())

        if layer_scheduler.is_priority_required:
            with_prio = True

    return (MLQ.create(layers), layer_names, with_prio)

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

    return (MLFQ.create(time_quantums, end_layer.create()), layer_names, with_prio)

def main():
    process_list: List[Process] = []
    scheduler_choices: List[Scheduler] = [FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF, MLQ, MLFQ] 
    
    print("===== CPU Scheduling Simulator =====")
    
    # Select a scheduler
    print(format_choice_list(list(map(lambda s : s.name, scheduler_choices))), end="\n\n")
    scheduler_choice = input_bounded_num("Select a scheduler: ", max=len(scheduler_choices))

    # Retrieve scheduler and its details
    scheduler_class: Scheduler = scheduler_choices[scheduler_choice - 1]
    with_prio: bool = scheduler_class.is_priority_required
    with_queue_level: bool = scheduler_class.is_queue_level_required

    # Configure chosen scheduler 
    time_quantum: int = 0
    layer_names: List[str] = []
    scheduler_instance = None

    print("\n=====", scheduler_class.name, "Configuration =====")
    if scheduler_class == RoundRobin:
        time_quantum = input_bounded_num("Time quantum: ") 
        scheduler_instance = scheduler_class.create(time_quantum, True)
        print()
    elif scheduler_class.is_multilevel:
        num_layers = input_bounded_num("Number of Layers: ")

        if scheduler_class == MLQ:
            scheduler_instance, layer_names, with_prio = configure_mlq(num_layers)
        elif scheduler_class == MLFQ:
            scheduler_instance, layer_names, with_prio = configure_mlfq(num_layers)
        
    else:
        print("Has no extra configuration required.")
        scheduler_instance = scheduler_class.create()
    print()

    # Configure processes to be processed
    num_of_processes = input_bounded_num("Number of processes: ")
    for _ in range(num_of_processes):
        os.system("cls")
        pid = next(Process.id_sequence)

        print("===== P" + str(pid) + " Details =====")
        if scheduler_class.is_queue_level_required:
            print(format_choice_list(layer_names), end="\n\n")
        
        arrival_time = input_bounded_num("Arrival Time: ", 0) 
        burst_time = input_bounded_num("Burst Time: ")
        priority = input_bounded_num("Priority: ") if with_prio else 1
        queue_level = input_bounded_num("Queue Level: ") if with_queue_level else 1

        process = Process(pid, arrival_time, burst_time, priority, queue_level - 1)
        process_list.append(process)

    # Instantiate operating system simulator with the given schedueler instance and processes
    oss = OS(scheduler_instance, process_list)
    oss.run()

    # Print details of the configured scheduler, the results of execution, and metrics
    os.system("cls")
    print("===== CPU Scheduling Simulator =====")
    print("Scheduler: ", scheduler_class.name, " | q=" + str(time_quantum) if scheduler_class == RoundRobin else "")
    if scheduler_class.is_multilevel:
        print()
        print("# LAYER CONFIGURATION")
        print(format_choice_list)

    print()
    print_metrics(oss, with_prio, scheduler_class.is_queue_level_required, layer_names)
    
if __name__ == "__main__":
    main()