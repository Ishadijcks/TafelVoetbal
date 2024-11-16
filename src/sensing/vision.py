import cv2
from picamera2 import Picamera2
from libcamera import controls as cam_controls

from communication.commands.commands import StickId
from model.game_state import GameState
from sensing.frame_analysis import frame_analysis
from sensing.sensor import Sensor


class Vision(Sensor):
    def __init__(self):
        self.picam2 = Picamera2()
        main = {
            'size': (500, 500),
        }

        MAX_WIDTH, MAX_HEIGHT = self.picam2.camera_properties['PixelArraySize']

        margin_top = 0.0
        margin_left = 0.0
        margin_right = 0.0
        margin_bottom = 0.0

        raw = {
            'size': (1200, 1200),
        }
        controls = {
            'AfMode': cam_controls.AfModeEnum.Continuous,
            'FrameRate': 50,
            'ExposureTime': 2500,
            'ScalerCrop': (
                int(margin_left * MAX_WIDTH), int(margin_top * MAX_HEIGHT),
                int((1 - margin_left - margin_right) * MAX_WIDTH),
                int((1 - margin_top - margin_bottom) * MAX_HEIGHT))
        }
        config = self.picam2.create_video_configuration(main, raw=raw, controls=controls)
        self.picam2.configure(config)
        print(self.picam2.camera_configuration())
        self.picam2.start()

    def get_state(self, delta: float) -> GameState:
        frame = self.picam2.capture_array()

        center, radius, frame = frame_analysis(frame)
        cv2.imshow("Wajooo", frame)
        key = cv2.waitKey(1) & 0xFF

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