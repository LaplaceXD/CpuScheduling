# Operating System Concepts - CS 3104 Project

A program used to simulate various operating system concepts, such as:
1. `CPU Process Scheduling`, wherein a process scheduling algorithm is simulated on a single-core processor. The scheduler, and the processes are manually configured by the user to understand, how operating systems ensure fairness, responsitivity, and other metrics within the system.
2. `Memory Page Replacement Algorithms`, wherein a memory page replacement algorithm is simulated based on a set of incoming page references. The algorithm, and page references are manually configured by the user to understand how pages are swapped in and out to ensure higher page hits.

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

**Scheduling algorithms** are used to manage the execution of processes in an operating system ensuring fairness, quick response times, maximized average turnaround time, minimized average waiting time, and other criteria. These algorithms can be preemptive or non-preemptive. 

Preemptive scheduling algorithms allow the interruption of currently executing processes to start or resume another process, while non-preemptive scheduling algorithms do not permit such interruptions, requiring the currently running process to complete its execution before the next one starts.

### List of Scheduling Algorithms Implemented:
| Page Replacement Algorithm           | Replacement Criteria                         |
| ------------------------------------ | -------------------------------------------- |
| First-In, First-Out (FIFO)           | Arrival Time                                 |
| Least Recently Used (LRU)            | Recency of Usage                             |
| Least Frequently Used (LFU)          | Frequency of Usage during its time in Memory |
| Optimal                              | Interval of Next Usage of the Page           |

## Setup / Usage

**Prerequisites:** Make sure you have [`Python`](https://www.python.org/downloads/) installed.
1. Clone this repository.
2. `cd` into the cloned repository.
3. Run `py main.py` in the terminal.

## Contributing

Unfortunately, we are not accepting pull requests, since this is a one-time project. However, feel free to fork this project, and improve on it!

## License

[GNU General Public License v3.0](https://github.com/LaplaceXD/CpuScheduling/blob/master/LICENSE)
