import os
from scheduling_sim.main import main as scheduling_main
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
    
    os.system("cls")
    entries[choice - 1]()

if __name__ == "__main__":
    main()