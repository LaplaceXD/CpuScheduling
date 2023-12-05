# Operating System Concepts - CS 3104 Project

A program used to simulate various operating system concepts, such as:
1. `CPU Process Scheduling`, wherein a process scheduling algorithm is simulated on a single-core processor. The scheduler and the processes are manually configured by the user to understand, how operating systems ensure fairness, responsitivity, and other metrics within the system.
2. `Memory Page Replacement Algorithms`, wherein a memory page replacement algorithm is simulated based on a set of incoming page references. The algorithm and page references are manually configured by the user to understand how pages are swapped in and out to ensure higher page hits.

These simulations were created in partial fulfillment of the requirements of one of my course requirements, **CS 3104 - Operating Systems**.

## Process Scheduling Algorithms

**Scheduling algorithms** are used to manage the execution of processes in an operating system ensuring fairness, quick response times, maximized average turnaround time, minimized average waiting time, and other criteria. These algorithms can be preemptive or non-preemptive. 

Preemptive scheduling algorithms allow the interruption of currently executing processes to start or resume another process, while non-preemptive scheduling algorithms do not permit such interruptions, requiring the currently running process to complete its execution before the next one starts.

### List of Scheduling Algorithms Implemented:
| Scheduling Algorithm                 | Preemptive | Scheduling Criteria               |
| ------------------------------------ | ---------- | --------------------------------- |
| First-Come-First-Serve (FCFS)        | No         | Arrival time                      |
| Shortest Job First (SJF)             | No         | Burst time (execution time)       |
| Priority Non-Preemptive (Prio-NP)    | No         | Priority assigned to each process |
| Priority Preemptive (Prio-P)         | Yes        | Priority assigned to each process |
| Round Robin (RR)                     | Yes        | Time quantum                      |
| Shortest Remaining Time First (SRTF) | Yes        | Remaining Burst Time              |
| Multilevel Queue (MLQ)               | Yes        | Queue Levels                      |
| Multilevel Feedback Queue (MLFQ)     | Yes        | Feedback mechanism                |


### Limitation
While the scheduling algorithm here works, it doesn't take into account I/O time of processes.

## Page Replacement Algorithms (Memory Management)

**Page replacement algorithms** are essential components of operating systems that manage the swapping of pages in and out of memory. Their primary goal is to optimize memory utilization, minimize page faults, and enhance overall system performance. These algorithms are categorized as either global or local.

In a global page replacement algorithm, the operating system considers all pages across the entire system when deciding which page to replace. On the other hand, local page replacement algorithms base their decisions on the pages within the specific process that generated the page fault.

### List of Page Replacement Algorithms Implemented:
| Page Replacement Algorithm           | Replacement Criteria                         |
| ------------------------------------ | -------------------------------------------- |
| First-In, First-Out (FIFO)           | Arrival Time                                 |
| Least Recently Used (LRU)            | Recency of Usage                             |
| Least Frequently Used (LFU)          | Frequency of Usage during its time in Memory |
| Optimal                              | Interval of Next Usage of the Page           |

### Proof of Concept
If you only want to see the algorithms and their implementation without all the unnecessary presentation layers found in this repository. You can check out this [proof of concept](https://pastebin.com/trLMDbqa) paste bin that I created.

# Disk Scheduling Algorithms

**Disk scheduling algorithms** are crucial components of operating systems that manage the efficient positioning of disk read/write heads to optimize access times for disk I/O operations. These algorithms aim to minimize seek time, enhance overall system performance, and improve the utilization of the disk.

These algorithms can be categorized based on their approach to scheduling disk I/O requests. Common disk scheduling algorithms include First Come First Serve (FCFS), Shortest Seek Time First (SSTF), SCAN, C-SCAN, LOOK, and C-LOOK.

### List of Disk Scheduling Algorithms Implemented:
| Disk Scheduling Algorithm           | Scheduling Criteria                        |
| ------------------------------------ | ------------------------------------------ |
| First Come First Serve (FCFS)        | Arrival Time of Disk I/O Requests          |
| Shortest Seek Time First (SSTF)      | Minimum Seek Time to Reach the Requested Track |
| SCAN                                 | Seek in One Direction Until Outer Track is Reached, Then Reverse Direction |
| C-SCAN                               | Seek in One Direction Until Outer Track is Reached, Jump to the Inner Track, and Repeat |
| LOOK                                 | Seek in One Direction Until No More Requests in That Direction, Then Reverse Direction |
| C-LOOK                               | Seek in One Direction Until No More Requests in That Direction, Then Seek to The Lowest Track|

### Proof of Concept
If you only want to see the algorithms and their implementation without all the unnecessary presentation layers found in this repository. You can check out this [proof of concept](https://pastebin.com/HRi8TEC3) paste bin that I created.

### Jupyter Notebook Alternative
If you are more comfortable working with `Jupyter Notebooks`, you can make use of the [notebook](https://github.com/LaplaceXD/OperatingSystemConcepts/blob/master/disk-scheduling.ipynb) I uploaded to this repository to try out the disk scheduling algorithms.

## Setup / Usage

**Prerequisites:** Make sure you have [`Python`](https://www.python.org/downloads/) installed.
1. Clone this repository.
2. `cd` into the cloned repository.
3. Run `py main.py` in the terminal.

## Contributing

Unfortunately, I am not accepting pull requests, since this is a one-time project. However, feel free to fork this project, and improve on it!

## License

[GNU General Public License v3.0](https://github.com/LaplaceXD/CpuScheduling/blob/master/LICENSE)
