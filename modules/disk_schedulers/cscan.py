from typing import List

def cscan(tracks: List[int], track_bounds: tuple[int, int]):
    higher_tracks = sorted(track for track in tracks if track >= tracks[0])
    lower_tracks = sorted(track for track in tracks[1:] if track < tracks[0])

    if len(lower_tracks) > 0:
        if track_bounds[1] not in higher_tracks:
            higher_tracks.append(track_bounds[1])
        if track_bounds[0] not in lower_tracks:
            lower_tracks.insert(0, track_bounds[0])

    return higher_tracks + lower_tracks