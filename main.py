import os

from scheduling import main as scheduling_main
from utils.io import input_bounded_num
from views import View

def main():
    choices = [
        "CPU Scheduling",
    ]
    
    entries = [
        scheduling_main,
    ]

    print("===== Operating System Simulator =====")
    print(View.numbered_list(choices))
    print()
    print("What do you want to simulate?")
    choice = input_bounded_num("Choice: ", max=len(choices))
    

    is_interrupted = False 
    while not is_interrupted:
        os.system("cls")
        entries[choice - 1]()
        
        status = input("\n\nContinue (type quit to exit)...")
        if status and status.lower() == "quit":
            is_interrupted = True

if __name__ == "__main__":
    main()