import cv2
import os
import numpy as np

import json


def pred_moving_plate(image):
    out = 0
    with open('/home/aspagteq/Documents/after_assembly/test_vision/muvro/movingplate.json', 'r') as openfile:
        r = json.load(openfile)

    with open('/home/aspagteq/Documents/after_assembly/test_vision/muvro/movingplatethrust.json', 'r') as openfile:
        mi, mx = json.load(openfile)

    try:
        img = cv2.imread(image)
    except:
        img = image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.rectangle(img, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), 255, 1)

    roi = gray[int(r[1]):int(r[1]+r[3]),
               int(r[0]):int(r[0]+r[2])]
    edge = cv2.Canny(roi, 90, 250)

    n_white = np.count_nonzero(edge == 255)
    edge = cv2.resize(edge, (400, 400))

    if mi > n_white:
        img = cv2.putText(img, "NG", (20, 50),
                          cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        img = cv2.rectangle(img, (r[0], r[1]),
                            (r[0]+r[2], r[1]+r[3]), (0, 0, 255), 3)
        overlay = np.zeros_like(img)
        overlay[:] = (0, 0, 255)

    elif mx < n_white:
        img = cv2.putText(img, "NG", (20, 50),
                          cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        img = cv2.rectangle(img, (r[0], r[1]),
                            (r[0]+r[2], r[1]+r[3]), (0, 0, 255), 3)
        overlay = np.zeros_like(img)
        overlay[:] = (0, 0, 255)

    else:
        img = cv2.putText(img, "OK", (20, 50),
                          cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        out = 1
        overlay = np.zeros_like(img)
        overlay[:] = (0, 255, 0)

    img = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    return img, out


if __name__ == "__main__":

    from cam import camera_streams
    cap = camera_streams(mode="Industrial")

    while True:
        frame = cap.get_frame((680, 500))
        img, out = pred_moving_plate(frame)
        cv2.imshow("img", img)
        if cv2.waitKey(2) == ord('q'):
            break
    cv2.destroyAllWindows()

