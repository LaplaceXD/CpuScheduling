import os

from utils.io import input_bounded_num
from views import View

def main():
    choices = [
        "CPU Scheduling",
        "Memory Management",
        "Disk Scheduling"
    ]

    print("===== Operating System Simulator =====")
    print(View.numbered_list(choices))
    print()
    print("What do you want to simulate?")
    choice = input_bounded_num("Choice: ", max=len(choices)) - 1

    entry_fn = None
    if choices[choice] == choices[0]: from process_scheduling import main as entry_fn
    if choices[choice] == choices[1]: from memory_managing import main as entry_fn
    if choices[choice] == choices[2]: from disk_scheduling import main as entry_fn

    is_running = True 
    while is_running:
        os.system("cls") 
        entry_fn()
        
        status = input("\n\nContinue (type quit to exit)...")
        if status and status.lower() == "quit":
            is_running = False

if __name__ == "__main__":
    main()
