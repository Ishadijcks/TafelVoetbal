import cv2

from communication.commands.commands import StickId
from model.game_state import GameState
from sensing.frame_analysis import frame_analysis
from sensing.sensor import Sensor


class PiCamera(Sensor):

    def __init__(self):
        from picamera2 import Picamera2
        from libcamera import controls as cam_controls

        self.last_center = None
        self.picam2 = Picamera2()

        main = {
            'size': (500, 500),
            'format': 'RGB888',
        }

        MAX_WIDTH, MAX_HEIGHT = self.picam2.camera_properties['PixelArraySize']

        margin_top = 0.14
        margin_left = 0.03
        margin_right = 0.05
        margin_bottom = 0.06

        raw = {
            'size': (1200, 1200),
        }
        controls = {
            'AfMode': cam_controls.AfModeEnum.Continuous,
            'FrameRate': 50,
            # 'ExposureTime': 2500,
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

        if self.last_center and center:
            ball_x, ball_y = center
            prev_ball_x, prev_ball_y = self.last_center
            prediction_x = ball_x + (ball_x - prev_ball_x)
            prediction_y = ball_y + (ball_y - prev_ball_y)
            cv2.circle(frame, (int(prediction_x*frame.shape[0]), int(prediction_y*frame.shape[1])), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, int(radius), (0, 0, 255), -1)

        cv2.imshow("Wajooo", frame)
        cv2.waitKey(1)

        if not center:
            return GameState()

        self.last_center = center

        return GameState(
            sticks={
                StickId.ONE: 0,
                StickId.TWO: 0,
                StickId.THREE: 0,
                StickId.FOUR: 0,
            },
            ball=center
        )
