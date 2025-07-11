import numpy as np
import cv2
from collections import deque

def setValues(x):
    pass

cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)

# Color arrays
colors = [
    (255, 0, 0),     # Blue
    (0, 255, 0),     # Green
    (0, 0, 255),     # Red
    (0, 255, 255),   # Yellow
    (128, 0, 128),   # Purple
    (0, 165, 255)    # Orange
]

color_names = ["BLUE", "GREEN", "RED", "YELLOW", "PURPLE", "ORANGE"]

# Color deques
points = [ [deque(maxlen=1024)] for _ in colors ]
indices = [0]*len(colors)
colorIndex = 0
kernel = np.ones((5, 5), np.uint8)

paintWindow = np.zeros((471, 636, 3)) + 255
btn_y1, btn_y2 = 1, 65
for i in range(len(colors)):
    x1, x2 = 10 + i*100, 100 + i*100
    paintWindow = cv2.rectangle(paintWindow, (x1, btn_y1), (x2, btn_y2), colors[i], -1)
    cv2.putText(paintWindow, color_names[i], (x1+10, btn_y1+35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

# Clear Button
paintWindow = cv2.rectangle(paintWindow, (610, btn_y1), (635, btn_y2), (0, 0, 0), -1)
cv2.putText(paintWindow, "X", (615, btn_y1+35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue, u_saturation, u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])

    # Add buttons to frame (top)
    for i in range(len(colors)):
        x1, x2 = 10 + i*100, 100 + i*100
        frame = cv2.rectangle(frame, (x1, 1), (x2, 65), colors[i], -1)
        cv2.putText(frame, color_names[i], (x1+10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    # Clear button
    frame = cv2.rectangle(frame, (610, 1), (635, 65), (0, 0, 0), -1)
    cv2.putText(frame, "X", (615, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # Detect marker
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
        cv2.circle(frame, center, int(radius), (0, 255, 255), 2)

        if center[1] <= 65:
            for i in range(len(colors)):
                if 10 + i*100 <= center[0] <= 100 + i*100:
                    colorIndex = i
            if 610 <= center[0] <= 635:
                points = [[deque(maxlen=1024)] for _ in colors]
                indices = [0]*len(colors)
                paintWindow[67:,:,:] = 255
        else:
            points[colorIndex][indices[colorIndex]].appendleft(center)
    else:
        for i in range(len(colors)):
            points[i].append(deque(maxlen=1024))
            indices[i] += 1

    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask", Mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
