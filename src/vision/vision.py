import os

from dotenv import load_dotenv, find_dotenv
import cv2
from picamera2 import Picamera2
from libcamera import controls as cam_controls

def vision():
    picam2 = Picamera2()
    main = {
        'size': (500, 500),
    }

    MAX_WIDTH, MAX_HEIGHT = picam2.camera_properties['PixelArraySize']

    margin_top = 0.1
    margin_left = 0.3
    margin_right = 0.3
    margin_bottom = 0.1

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
    config = picam2.create_video_configuration(main, raw=raw, controls=controls)
    picam2.configure(config)
    print(picam2.camera_configuration())
    picam2.start()

    print('actual crop', picam2.camera_controls['ScalerCrop'])
    while True:

        frame = picam2.capture_array()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # TODO(@Isha): Get Qt preview working or make this configurable
        cv2.imshow('frame', frame)

        # Close down the video stream
        cv2.destroyAllWindows()


def main():
    load_dotenv(find_dotenv())

    print(os.getenv("TOPIC"))


if __name__ == '__main__':
    main()
