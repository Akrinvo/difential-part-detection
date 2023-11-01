import cv2
import os
import numpy as np
import json


def hconcat_resize(img_list,
                   interpolation=cv2.INTER_CUBIC):
    # take minimum hights
    h_min = min(img.shape[0]
                for img in img_list)

    # image resizing
    im_list_resize = [cv2.resize(img,
                                 (int(img.shape[1] * h_min / img.shape[0]),
                                  h_min), interpolation=interpolation)
                      for img in img_list]

    # return final image
    return cv2.hconcat(im_list_resize)

# function is for concatinate the image vertically


def vconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    # take minimum width
    w_min = min(img.shape[1]
                for img in img_list)

    # resizing images
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
        interpolation=interpolation)
        for img in img_list]
    # return final image
    return cv2.vconcat(im_list_resize)


def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #                 print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName


def pred_pins(image):
    with open('/home/aspagteq/Documents/after_assembly/test_vision/muvro/pinsparam.json', 'r') as openfile:
        pinparam = json.load(openfile)

    with open('/home/aspagteq/Documents/after_assembly/test_vision/muvro/pin.json', 'r') as openfile:
        pin = json.load(openfile)
    out = 0

    try:
        img1 = cv2.imread(image)
    except:
        img1 = image

    shv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    rois = []
    count = 0
    thresh = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)[1]
    g = cv2.cvtColor(shv, cv2.COLOR_BGR2GRAY)

    hsvthresh = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    for r, j in zip(pin, range(1, 5)):

        img = cv2.rectangle(img, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), 255, 1)
        roi = thresh[int(r[1]):int(r[1]+r[3]),
                     int(r[0]):int(r[0]+r[2])]
        croi = hsvthresh[int(r[1]):int(r[1]+r[3]),
                         int(r[0]):int(r[0]+r[2])]

        roi = cv2.resize(roi, (61, 61))

        pin_black = np.count_nonzero(roi == 255)

        if (pinparam[f"min{j}"] - pin_black)>450:
            print(j,pinparam[f"min{j}"],pin_black)
            count += 1
            img1 = cv2.rectangle(
                img1, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), (0, 0, 255), 3)
            overlay = np.zeros_like(img1)
            overlay[:] = (0, 0, 255)

        else:
            img1 = cv2.rectangle(
                img1, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), 255, 2)
            # print(pinparam[f"min{j}"],f" {j} ",pin_black)

        rois.append(roi)

    img = cv2.putText(img1, str(
        count), (img1.shape[0]-1, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
    if count > 0:
        img1 = cv2.putText(img1, "NG", (20, 50),
                           cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        # img1 = cv2.rectangle(img1, (r[0], r[1]),
        #                      (r[0]+r[2], r[1]+r[3]), (0, 0, 255), 3)
        overlay = np.zeros_like(img1)
        overlay[:] = (0, 0, 255)
    else:
        img1 = cv2.putText(img1, "OK", (20, 50),
                           cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        img1 = cv2.rectangle(img1, (r[0], r[1]),
                             (r[0]+r[2], r[1]+r[3]), 255, 2)
        out = 1
        overlay = np.zeros_like(img1)
        overlay[:] = (0, 255, 0)
    roiss = vconcat_resize(rois)
    roiss = cv2.resize(roiss, (150, 600))
    img1 = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    # cv2.imshow("roiss",roiss)
    return img1, out


if __name__ == "__main__":
    from cam import camera_streams
    cap = camera_streams(mode="Industrial")

    while True:
        frame = cap.get_frame((680, 500))
        img, out = pred_pins(frame)
        cv2.imshow("img", img)
        if cv2.waitKey(2) == ord('q'):
            break
    cv2.destroyAllWindows()
