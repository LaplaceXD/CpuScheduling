from typing import List

def look(tracks: List[int], track_bounds: tuple[int, int]):
    higher_tracks = sorted(track for track in tracks if track >= tracks[0])
    lower_tracks = sorted((track for track in tracks[1:] if track < tracks[0]), reverse=True)

    return higher_tracks + lower_tracks