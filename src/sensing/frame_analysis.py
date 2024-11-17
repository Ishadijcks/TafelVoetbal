import cv2
import imutils


def frame_analysis(frame) -> ((int, int), int, any):
    """Returns (center, radius, frame)"""
    redLowerHSV = (135, 152, 110)
    redUpperHSV = (214, 255, 255)

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "red", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, redLowerHSV, redUpperHSV)
    mask = cv2.dilate(mask, None, iterations=4)
    mask = cv2.erode(mask, None, iterations=4)

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

        # TODO check why this happens
        if M["m00"] == 0:
            M["m00"] = 0.001
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, int(radius), (0, 0, 255), -1)

            relative_x = center[0] / frame.shape[1]
            relative_y = center[1] / frame.shape[0]
            cv2.putText(frame, f"x: {relative_x}, y: {relative_y}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255),
                        thickness=2)
            return (relative_x, relative_y), radius, frame
    return None, 0, frame
