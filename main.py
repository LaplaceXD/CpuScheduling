import os

from process_scheduling import main as scheduling_main
from memory_managing import main as memory_managing_main
from utils.io import input_bounded_num
from views import View

def main():
    choices = [
        "CPU Scheduling",
        "Memory Management"
    ]
    
    entries = [
        scheduling_main,
        memory_managing_main
    ]

    print("===== Operating System Simulator =====")
    print(View.numbered_list(choices))
    print()
    print("What do you want to simulate?")
    choice = input_bounded_num("Choice: ", max=len(choices))
    
    is_running = True 
    while is_running:
        os.system("cls")
        entries[choice - 1]()
        
        status = input("\n\nContinue (type quit to exit)...")
        if status and status.lower() == "quit":
            is_running = False

if __name__ == "__main__":
    main()
