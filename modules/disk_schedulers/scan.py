from typing import List

def scan(tracks: List[int], track_bounds: tuple[int, int]):
    higher_tracks = sorted(track for track in tracks if track >= tracks[0])
    lower_tracks = sorted((track for track in tracks[1:] if track < tracks[0]), reverse=True)

    if len(lower_tracks) > 0 and track_bounds[1] not in higher_tracks:
        higher_tracks.append(track_bounds[1])

    return higher_tracks + lower_tracks