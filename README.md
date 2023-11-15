# CPU Scheduling Algorithms - CS 3104 Project

A program used to simulate how schedulers work on an operating system running on a single-core processor. Users can give a set of processes, and select the scheduling algorithm to be used by the processor to simulate how the OS runs. This was created in partial fulfillment of the requirements of one of my course requirements, **CS 3102 - Operating Systems**.

## Scheduling Algorithms

**Scheduling algorithms** are used to manage the execution of processes in an operating system ensuring fairness, quick response times, maximized average turnaround time, minimized average waiting time and other criteria. These algorithms can be preemptive or non-preemptive. 

Preemptive scheduling algorithms allow the interruption of currently executing processes to start or resume another process, while non-preemptive scheduling algorithms do not permit such interruptions, requiring the currently running process to complete its execution before the next one starts.

### List of Scheduling Algorithms Implemented:
| Scheduling Algorithm              | Preemptive | Scheduling Criteria              |
| --------------------------------- | -----------| ---------------------------------|
| First-Come-First-Serve (FCFS)      | No         | Arrival time                     |
| Shortest Job First (SJF)           | No         | Burst time (execution time)      |
| Priority Non-Preemptive (Prio-NP)  | No         | Priority assigned to each process|
| Priority Preemptive (Prio-P)       | Yes        | Priority assigned to each process|
| Round Robin (RR)                   | Yes        | Time quantum                    |
| Shortest Remaining Time First (SRTF) | Yes      | Remaining Burst Time             |
| Multilevel Queue Scheduling (MLQ) | Varies     | Queue Levels                    |
| Multilevel Feedback Queue (MLFQ)   | Varies     | Feedback mechanism              |


### Limitation
While the scheduling algorithm here works, it doesn't take into account I/O time, and memory allocation of processes.

## Setup / Usage

**Prerequisites:** Make sure you have [`Python`](https://www.python.org/downloads/) installed.
1. Clone this repository.
2. `cd` into the cloned repository.
3. Run `py main.py` in the terminal.

## Contributing

Unfortunately, we are not accepting pull requests, since this is a one-time project. However, feel free to fork this project, and improve on it!

## License

[GNU General Public License v3.0](https://github.com/LaplaceXD/CpuScheduling/blob/master/LICENSE)