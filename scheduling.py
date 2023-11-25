import os
from typing import List

from models import Process, ProcessLog
from modules import Processor, Clock
from modules.schedulers import Scheduler, FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF, MLQ, MLFQ
from views import View, TableView, GanttView
from utils.io import input_bounded_num

def create_process_execution_gantt(process_dump: List[ProcessLog], layers: List[str] = []):
    layer_gantts = [GanttView(name="[{}]".format(i + 1), show_timestamps=i + 1 == len(layers)) for i in range(len(layers))]
    merged_gantt = GanttView(name="[A]" if len(layers) > 0 else None)
    for log in process_dump:
        name = "P" + str(log.name) if type(log.name) == int else log.name
        time = log.end

        for tag, layer_gantt in enumerate(layer_gantts):
            layer_gantt.add_item(name if log.tag == tag else "", time)

        merged_gantt.add_item(name, time)

    return merged_gantt, layer_gantts

def create_os_metrics(processes: List[Process], total_run_time: int, total_idle_time: int):
    metrics = ""
    
    metrics += "CPU Utilization: {:.2f}%\n".format((float(total_run_time - total_idle_time) / float(total_run_time)) * 100)
    metrics += "Average TAT: {:.2f}\n".format(sum(p.turnaround for p in processes) / len(processes))
    metrics += "Average WT: {:.2f}".format(sum(p.waiting for p in processes) / len(processes))
    
    return metrics

def create_process_table_summary(processes: List[Process], has_priority_field: bool, has_queue_level_field: bool):
    table_headers = ["PID", "AT", "BT", "CT", "TAT", "WT"] 
    if has_priority_field:
        # Insert at the index before CT
        idx = len(table_headers) - 3 
        table_headers.insert(idx, "Prio")
    
    if has_queue_level_field:
        # Insert at the index before CT
        idx = len(table_headers) - 3 
        table_headers.insert(idx, "QL")

    table = TableView(header=table_headers)
    
    for p in processes:
        data = ["P" + str(p.pid), p.arrival, p.burst, p.completion, p.turnaround, p.waiting]
        if has_priority_field:
            # Insert at the index before p.completion
            idx = len(data) - 3 
            data.insert(idx, p.priority)
    
        if has_queue_level_field:
            # Insert at the index before p.completion
            idx = len(data) - 3 
            data.insert(idx, p.queue_level + 1)

        table.add_item(*data)
    
    return table

def configure_mlq(num_layers: int):
    has_priority_field = False
    layers = []
    layer_names = []
    layer_choices = MLQ.layer_choices()
    
    print(View.numbered_list(map(lambda s : s.name, layer_choices)))
    for layer_num in range(num_layers):
        scheduler_choice = input_bounded_num("Layer #{}: ".format(layer_num + 1), max=len(layer_choices))

        layer_scheduler = layer_choices[scheduler_choice - 1]
        if layer_scheduler == RoundRobin:
            time_quantum = input_bounded_num("Time quantum: ") 
            layer_names.append(layer_scheduler.name + " | q=" + str(time_quantum))
            layers.append(layer_scheduler.factory(time_quantum, False))
        else:
            layer_names.append(layer_scheduler.name)
            layers.append(layer_scheduler.factory())

        if layer_scheduler.has_priority_field:
            has_priority_field = True

    return MLQ.factory(layers), layer_names, has_priority_field

def configure_mlfq(num_layers: int):
    allowed_last_layers = MLFQ.last_layer_choices()
    layer_names = []
    time_quantums = []

    for i in range(num_layers - 1):
        layer_time_quantum = input_bounded_num("RR #{} - Time Quantum: ".format(i + 1))
        time_quantums.append(layer_time_quantum)
        layer_names.append(RoundRobin.name + " | q=" + str(layer_time_quantum))

    print()
    print(View.numbered_list(map(lambda s : s.name, allowed_last_layers)), end="\n\n")
    selected_end_layer = input_bounded_num("Select End Layer: ", max=len(allowed_last_layers))
    
    end_layer = allowed_last_layers[selected_end_layer - 1]
    layer_names.append(end_layer.name)
    has_priority_field = end_layer.has_priority_field

    return MLFQ.factory(time_quantums, end_layer.factory()), layer_names, has_priority_field

def main():
    print("===== CPU Scheduling Simulator =====")
    
    # Select a scheduler
    scheduler_choices: List[Scheduler] = [FCFS, SJF, PriorityNP, Priority, RoundRobin, SRTF, MLQ, MLFQ] 
    print(View.numbered_list(map(lambda s : s.name, scheduler_choices)), end="\n\n")
    scheduler_choice = input_bounded_num("Select a scheduler: ", max=len(scheduler_choices))

    chosen_scheduler: Scheduler = scheduler_choices[scheduler_choice - 1]
    has_priority_field: bool = chosen_scheduler.has_priority_field
    has_queue_level_field: bool = chosen_scheduler.has_queue_level_field

    # Configure the chosen scheduler
    time_quantum: int = 0
    layer_names: List[str] = []
    scheduler_factory = None

    print("\n=====", chosen_scheduler.name, "Configuration =====")
    if chosen_scheduler == RoundRobin:
        time_quantum = input_bounded_num("Time quantum: ") 
        scheduler_factory = chosen_scheduler.factory(time_quantum, True)
    elif chosen_scheduler.is_multilevel:
        num_layers = input_bounded_num("Number of Layers: ")

        if chosen_scheduler == MLQ:
            scheduler_factory, layer_names, has_priority_field = configure_mlq(num_layers)
        elif chosen_scheduler == MLFQ:
            scheduler_factory, layer_names, has_priority_field = configure_mlfq(num_layers)
    else:
        print("Has no extra configuration required.")
        scheduler_factory = chosen_scheduler.factory()
    print()

    # Configure processes to be processed
    process_list: List[Process] = []
    num_of_processes = input_bounded_num("Number of processes: ")
    for pid in range(num_of_processes):
        os.system("cls")

        print("===== P" + str(pid + 1) + " Details =====")
        if has_queue_level_field:
            print(View.numbered_list(layer_names), end="\n\n")
        
        arrival_time = input_bounded_num("Arrival Time: ", 0) 
        burst_time = input_bounded_num("Burst Time: ")
        priority = input_bounded_num("Priority: ") if has_priority_field else 1
        queue_level = input_bounded_num("Queue Level: ") if has_queue_level_field else 1

        process = Process(pid + 1, arrival_time, burst_time, priority, queue_level - 1)
        process_list.append(process)

    # Simulate a running operating system
    clock = Clock(start_time=-1) # -1 = not started
    processor = Processor(clock=clock)
    scheduler = scheduler_factory(process_list, processor)

    while any(map(lambda p : not p.is_marked_completed, process_list)):
        clock.tick()

        if processor.is_occupied:
            processor.run()
            
            if processor.is_finished:
                completed_process = processor.clear()
                completed_process.mark_completed_on(clock.time) 

        ready_queue = scheduler.run(clock.time)

        if len(ready_queue) > 0 and processor.is_idle:
            process = ready_queue.pop(0)
            processor.load(process)

    # Print details of the configured scheduler, the results of execution, and metrics
    os.system("cls")
    print("===== CPU Scheduling Simulator =====")
    print("Scheduler: ", scheduler.name, " | q=" + str(time_quantum) if scheduler == RoundRobin else "")
    if scheduler.is_multilevel:
        print()
        print("# LAYER CONFIGURATION")
        print(View.numbered_list(layer_names))
    print()
    
    print("# PROCESS TABLE")
    table = create_process_table_summary(process_list, has_priority_field, has_queue_level_field)
    table.render()
    print()

    print("# GANTT CHART - TIMELINE")
    merged_gantt, layer_gantts = create_process_execution_gantt(processor.process_dump, layer_names)
    if len(layer_gantts) > 0:
        for layer_gantt in layer_gantts:
            layer_gantt.render()
        print()
    merged_gantt.render()
    print()

    print("# METRICS")
    metrics = create_os_metrics(process_list, total_run_time=clock.time, total_idle_time=processor.idle_time)
    print(metrics)

if __name__ == "__main__":
    main()