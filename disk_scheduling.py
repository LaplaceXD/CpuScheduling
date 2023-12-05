import re
from typing import List

from modules.disk_schedulers import fcfs, sstf, scan, cscan, look, clook
from views import View
from utils.io import input_bounded_num, input_choice

def graph_it(tracks: List[int], track_bounds: tuple[int, int], title: str = "", print_calcs_to_console: bool = False):
    import matplotlib.pyplot as plt
    
    time = list(range(len(tracks)))
    _, ax = plt.subplots()

    plt.plot(time, tracks, color="lightblue", linestyle="-", linewidth=2)
    plt.scatter(time, tracks, color="blue", marker="o", clip_on=False, zorder=2)
    
    for i, track in enumerate(tracks):
        ax.text(i, track + 7.5, track, color="blue", ha="center")
    
    plt.title(title)
    
    plt.xlabel("Time")
    plt.xticks(time)
    plt.xlim(0, time[-1])

    plt.ylabel("Track Number")
    y_ticks = [i for i in range(0, track_bounds[1], 20)]
    if track_bounds[1] not in y_ticks:
        y_ticks.append(track_bounds[1])
    plt.yticks(y_ticks)
    plt.ylim(track_bounds[0], track_bounds[1])
    
    seek_pairs = [(max(curr_track, next_track), min(curr_track, next_track)) for curr_track, next_track in zip(tracks[:-1], tracks[1:])]
    calculations = " + ".join(f"({curr} - {next})" for curr, next in seek_pairs)
    total_seek_time = sum(curr - next for curr, next in seek_pairs)

    if print_calcs_to_console:
        print(f"Total Seek Time = {calculations}")
        print(f"Total Seek Time = {total_seek_time}")
    else:
        plt.figtext(0.125, -0.05, f"Total Seek Time = {calculations}", fontsize = 10, ha="left", va="bottom")
        plt.figtext(0.125, -0.1, f"Total Seek Time = {total_seek_time}", fontsize = 10, ha="left", va="bottom")
    
    plt.grid(True)
    plt.show()

def main():
    print("===== Disk Scheduling Simulator =====")
    try:
        import matplotlib
    except:
        print("Matplotlib is required for this module. Use 'pip install matplotlib' to install it on your environment.")
        exit(1)
    
    num_cylinders = input_bounded_num("Number of Cylinders: ")
    track_bounds = (0, num_cylinders - 1)

    has_starting_track = input_choice("Has starting track?", choices=['Y', 'N'], default='N')
    starting_track = None
    if has_starting_track == 'Y':
        starting_track = input_bounded_num("Starting Track: ", min=track_bounds[0], max=track_bounds[1])
    
    tracks = []
    while len(tracks) == 0:
        track_list = input("Tracks (separated by space): ")
        tracks = re.findall(r'[A-Za-z0-9]+', track_list)
        if len(tracks) == 0:
            tracks.clear()
            print("Track list must not be empty!")
            continue

        try:
            tracks = [int(track) for track in tracks]
        except:
            tracks.clear()
            print("Tracks must only contain numbers.")

        for track in tracks:
            if track > track_bounds[1] or track < track_bounds[0]:
                tracks.clear()
                print(f"Tracks must be within the bounds of the tracks present, which is between {track_bounds[0]} and {track_bounds[1]}.")

    if starting_track is not None:
        tracks.insert(0, starting_track)

    choices = [
        ("First-Come, First-Serve (FCFS)", fcfs),
        ("Shortest Seek Time First", sstf),
        ("SCAN", scan),
        ("C-SCAN", cscan),
        ("LOOK", look),
        ("C-LOOK", clook),
    ]
    
    print()
    print(View.numbered_list(name for name, _ in choices))
    choice = input_bounded_num("Disk Scheduler: ", max=len(choices))
    disk_sched_name, disk_sched_fn = choices[choice - 1]

    sorted_tracks = disk_sched_fn(tracks, track_bounds)
    graph_it(sorted_tracks, track_bounds, disk_sched_name, print_calcs_to_console=True)

if __name__ == "__main__":
    main()