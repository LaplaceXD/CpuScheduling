import re
import os
from typing import List

from modules.memories import Memory, FIFO, LRU, LFU, Optimal
from modules import MemorySnapshot, MemoryMetrics
from views import View, TableView
from utils.io import input_bounded_num, input_choice

def main():
    print("===== Memory Management Simulator =====")

    # Create page references
    input_is_invalid = True
    pages = []
    while input_is_invalid:
        page_ref = input("Page Reference (separated by spaces): ")
        pages = re.findall(r'[A-Za-z0-9]+', page_ref)
        if len(pages) > 0:
            input_is_invalid = False
        else:
            print("Page reference needs to have at least one page.")
    pages = [int(page) if page.isdigit() else page for page in pages]

    # Selection of memory algorithms to use for simulation
    memory_choices: List[Memory] = [FIFO, LRU, LFU, Optimal]
    print(View.numbered_list(m.name for m in memory_choices), end="\n\n")
    
    is_selecting = True
    memories: List[tuple[Memory, List[MemorySnapshot]]] = [] 
    while is_selecting:
        memory_choice = input_bounded_num("Selected Memory: ", max=len(memory_choices))
        frame_size = input_bounded_num("Frame Size: ")
        
        chosen_memory = memory_choices[memory_choice - 1]
        memory_instance = chosen_memory(frame_size) if chosen_memory != Optimal else chosen_memory(frame_size, pages)
        if all(m != memory_instance for m, _ in memories):
            memories.append((memory_instance, []))
        else:
            print("Chosen memory configuration is a duplicate, it won't be added further.\n")

        # Prompt user if they want to continue selecting 
        select_another_choice = input_choice("Select another memory?", choices=["Y", "N"], default="N")        
        if select_another_choice == "N":
            is_selecting = False
        print()

    # Simulate a running paging process for all pagers
    for memory, paging_timeline in memories:
        for time, page in enumerate(pages, start=1):
            replaced_page, is_fault = memory.load(page)

            snapshot = MemorySnapshot(time, memory, page, replaced_page, is_fault)
            paging_timeline.append(snapshot)

    # Print details of execution of memory algos
    os.system("cls")
    print("===== MEMORY MANAGEMENT SIMULATOR =====")

    # Loop through each memory and print their details based on the snapshots recorded
    # Also keep track of metrics to be recorded later on for summarization
    memory_metrics: List[MemoryMetrics] = []
    for memory, paging_timeline in memories:
        metrics = MemoryMetrics(paging_timeline)
        memory_metrics.append(metrics)

        print("=====", memory.extended_name, "Simulation =====")
        page_ref_table = TableView()
        # This is to ensure that Pages header is aligned with the columns in Memory State Visualization
        row_header_pad = len("Frame {}".format(memory.frame_label_of(memory[0])))
        page_ref_table.add_item("{:>{}}".format("Pages", row_header_pad), *(page for page in pages))
        page_ref_table.render()
        print()

        print("## Memory State Visualization")
        print("Legend: F -> Page Fault | H -> Page Hit")
        table = TableView(header=["Time"] + [s.snapped_on for s in paging_timeline], footer=["Status"] + [s.status for s in paging_timeline])
        for frame in range(memory.capacity):
            row_header = "Frame {}".format(memory.frame_label_of(memory[frame]))
            table.add_item(row_header, *(s.snapshot[frame] if s.snapshot[frame] is not None else "--" for s in paging_timeline))
        table.render()
        print()
        
        print("## Performance Metrics")
        print("{:15}: {:<30}".format("No. of Hits", metrics.hits), end="")
        print("{:15}: {:<30}".format("Hit Ratio", metrics.hit_percent), end="\n")
        print("{:15}: {:<30}".format("No. of Faults", metrics.faults), end="")
        print("{:15}: {:<30}".format("Fault Ratio", metrics.fault_percent), end="\n")
        print()

        print("## Page State and Replacement Logs")
        print("State Format: {}".format(memory.state_annotation))
        print("Legend: {}".format(MemorySnapshot.log_legend))
        time_pad = max(len(str(s.snapped_on)) for s in paging_timeline)
        mem_state_pad = max(len(str(s.snapshot.state)) for s in paging_timeline)
        logs = [s.log(state_log_pad=mem_state_pad, time_log_pad=time_pad) for s in paging_timeline]
        logs.reverse()
        print(*logs, sep="\n")

        print("\n--------------------------------------------")

    # Summarize and rank the results of the memory simulation
    print()
    print("===== Summary Statistics =====")
    print("Legend: Ranked by page hits")
    print("Page References:", page_ref)

    memory_metrics.sort(key=lambda metric : metric.hits, reverse=True)
    summary_table = TableView(min_cell_width=8, header=["Rank#", "Page Replacement Algorithm", "Hits", "Faults", "Hit%", "Fault%"])
    for rank, metric in enumerate(memory_metrics, start=1):
        summary_table.add_item(rank, metric.memory_name, metric.hits, metric.faults, metric.hit_percent, metric.fault_percent)
    summary_table.render()

if __name__ == "__main__":
    main()