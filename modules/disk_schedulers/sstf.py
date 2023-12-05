from typing import List

def sstf(tracks: List[int], track_bounds: tuple[int, int]):
    tracks_buffer = tracks.copy()
    sorted_tracks = [tracks_buffer.pop(0)]

    while len(tracks_buffer) > 0:
        min_sstf_track_idx = min((i for i in range(len(tracks_buffer))), key=lambda i : abs(tracks_buffer[i] - sorted_tracks[-1]))
        track = tracks_buffer.pop(min_sstf_track_idx)
        sorted_tracks.append(track)

    return sorted_tracks