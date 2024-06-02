class Track:
    def __init__(self, start_pos: tuple[int, int], track_file: str, car_size: float):
        self.start_pos = start_pos
        self.track_file = track_file
        self.car_size = car_size
    
    @property
    def name(self):
        return self.track_file.split("/")[-1].split(".")[0]


tracks: list[Track] = [
    Track(start_pos=(600, 70), track_file="track-1.png", car_size=0.5),
    Track(start_pos=(700, 70), track_file="track-2.png", car_size=0.5),
    Track(start_pos=(500, 260), track_file="track-3.png", car_size=0.5)
]
