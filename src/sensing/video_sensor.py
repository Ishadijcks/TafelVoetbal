from collections import deque

import cv2

from communication.commands.commands import StickId
from model.game_state import GameState
from sensing.frame_analysis import frame_analysis
from sensing.sensor import Sensor


class VideoSensor(Sensor):
    """
    A fake sensor that reads a video as input.
    """

    pts = deque(maxlen=64)

    def __init__(self, path: str):
        super().__init__()
        self.total_time = 0.0
        self.video_stream = cv2.VideoCapture(path)

    def get_state(self, delta: float) -> GameState:
        frame = self.video_stream.read()[1]

        if frame is None:
            self.video_stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame = self.video_stream.read()[1]

        # TODO remove tang slice
        frame = frame[200:, :, :]

        center, radius, frame = frame_analysis(frame)

        cv2.imshow("Wajooo", frame)
        cv2.waitKey(1)

        if not center:
            return GameState()

        return GameState(
            sticks={
                StickId.ONE: 0,
                StickId.TWO: 0,
                StickId.THREE: 0,
                StickId.FOUR: 0,
            },
            ball=center
        )
