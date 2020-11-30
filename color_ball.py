import cv2
import numpy as np

position = [0, 0]

measures = []
bgr_color = []
hsv_color = []

roi = None


def on_on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y, x]
        print(position)


cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.setMouseCallback("Camera", on_on_mouse_click)


while cam.isOpened():
    ret, frame = cam.read()
    pxl_color = frame[position[0], position[1], :]
    measures.append(pxl_color)
    if len(measures) >= 10:
        bgr_color = np.uint8([[np.average(measures, 0)]])
        hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)[0][0]
        bgr_color = bgr_color[0][0]
        measures.clear()

    cv2.putText(frame, f'color = {bgr_color} {hsv_color}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (205, 92, 92))
    cv2.circle(frame, (position[1], position[0]), 5, (205, 92, 92))
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    cv2.imshow("Camera", frame)

cam.release()
cv2.destroyAllWindows()
