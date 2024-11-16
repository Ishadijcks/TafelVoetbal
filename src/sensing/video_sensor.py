from collections import deque

import cv2
import numpy as np

from communication.commands.commands import StickId
from model.game_state import GameState
from sensing.sensor import Sensor
import imutils


class VideoSensor(Sensor):
    """
    A fake sensor that reads a video as input.
    """
    redLowerHSV = (135, 152, 110)
    redUpperHSV = (214, 255, 255)

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

        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.redLowerHSV, self.redUpperHSV)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.erode(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        if center:
            relative_x = round(center[0] / frame.shape[1], 2)
            relative_y = round(center[1] / frame.shape[0], 2)
            cv2.putText(frame, f"x: {relative_x}, y: {relative_y}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, 10,
                        thickness=2, )
        else:
            relative_x = 0
            relative_y = 0
        # print(relative_x, relative_y)

        # update the points queue
        self.pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(self.pts)):
            # if either of the tracked points are None, ignore
            # them
            if self.pts[i - 1] is None or self.pts[i] is None:
                continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
            cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        cv2.imshow("Wajooo", frame)
        #
        key = cv2.waitKey(1) & 0xFF

        return GameState(
            sticks={
                StickId.ONE: 0,
                StickId.TWO: 0,
                StickId.THREE: 0,
                StickId.FOUR: 0,
            },
            ball=(relative_x, relative_y)
        )
