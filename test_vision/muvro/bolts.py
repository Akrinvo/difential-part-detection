
import cv2
import os
import numpy as np
import json
from cam import camera_streams
cap = camera_streams(mode="Industrial")


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


good = image_loc("muvro/sona_data")
# good=image_loc("sona_data/wbolt_wpin")


# pin=[[171, 146, 44, 45], [475, 160, 35, 38], [468, 326, 38, 38], [174, 319, 35, 36]]
pin = [[257, 194, 6, 5], [378, 168, 5, 3], [394, 235, 5, 5], [273, 263, 5, 6]]
bolt = [[328, 109, 26, 27], [359, 115, 25, 31], [386, 129, 25, 34], [408, 155, 22, 29], [419, 182, 23, 30], [423, 215, 21, 26], [412, 244, 23, 29], [393, 270, 28, 26], [367, 292, 33, 23], [341, 299, 30, 29], [
    309, 300, 29, 30], [280, 292, 30, 31], [255, 279, 27, 29], [237, 257, 24, 30], [226, 229, 27, 31], [225, 196, 22, 34], [232, 168, 26, 29], [247, 144, 21, 23], [267, 121, 31, 26], [293, 113, 36, 22]]

# param={"min1": 153, "max1": 219, "min2": 164, "max2": 223, "min3": 184, "max3": 255, "min4": 183, "max4": 259, "min5": 192, "max5": 252, "min6": 138, "max6": 245, "min7": 126, "max7": 237, "min8": 97, "max8": 230, "min9": 85, "max9": 252, "min10": 75, "max10": 210, "min11": 62, "max11": 187, "min12": 51, "max12": 209, "min13": 102, "max13": 253, "min14": 77, "max14": 245, "min15": 88, "max15": 238, "min16": 164, "max16": 256, "min17": 116, "max17": 240, "min18": 71, "max18": 217, "min19": 94, "max19": 256, "min20": 170, "max20": 286}
# param={'min1': 192, 'max1': 196, 'min2': 193, 'max2': 199, 'min3': 240, 'max3': 248, 'min4': 236, 'max4': 243, 'min5': 238, 'max5': 245, 'min6': 232, 'max6': 242, 'min7': 222, 'max7': 232, 'min8': 222, 'max8': 230, 'min9': 241, 'max9': 248, 'min10': 199, 'max10': 206, 'min11': 177, 'max11': 184, 'min12': 197, 'max12': 205, 'min13': 232, 'max13': 240, 'min14': 221, 'max14': 229, 'min15': 230, 'max15': 236, 'min16': 232, 'max16': 240, 'min17': 231, 'max17': 237, 'min18': 173, 'max18': 177, 'min19': 211, 'max19': 216, 'min20': 231, 'max20': 241}


param = {}
pins = {}
print(len(bolt))
pause = 0
# for i in good:
while (1):

    img1 = cap.get_frame((680, 500))

    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    img2 = img.copy()

    rois = []

    thresh = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)[1]

    cv2.imshow("thresh", thresh)

    k = cv2.waitKey(1)
    if k == ord('s'):
        pause = 1
        print("stop")
    if k == ord('p'):
        pause = 0
        print('play')
    if pause == 0:
        for r, j in zip(bolt, range(1, 21)):

            img1 = cv2.rectangle(
                img1, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), 255, 1)
            roi = thresh[int(r[1]):int(r[1]+r[3]),
                         int(r[0]):int(r[0]+r[2])]

            bl = cv2.medianBlur(roi, 9)

            roi = cv2.Canny(bl, 100, 180)

            rh, rw = roi.shape
            n_black = np.count_nonzero(roi == 255)

            if len(param) < 40:
                param[f"min{j}"] = n_black
                param[f"max{j}"] = n_black
            else:
                if param[f"min{j}"] > n_black:
                    param[f"min{j}"] = n_black
                if param[f"max{j}"] < n_black:
                    param[f"max{j}"] = n_black
            # print(n_white,n_black,rh*rw)
            rois.append(roi)

            # cv2.imshow(str(j),roi)
        # print("-----------------------------------------------------------------------------------")
        roiss = vconcat_resize([hconcat_resize(rois[:5]), hconcat_resize(
            rois[5:10]), hconcat_resize(rois[10:15]), hconcat_resize(rois[15:20])])
        roiss = cv2.resize(roiss, (400, 400))
        print(param)
        cv2.imshow("roiss", roiss)

        cv2.imshow("image", img1)
    if k == ord("q"):
        break
# while True:
#     frame=cap.get_frame((680,500))
#     cv2.imshow("img",img)
#     if cv2.waitKey(200)==ord('q'):break
cv2.destroyAllWindows()
print(param)


# param=json.dumps(param)
# with open("muvro/boltsparam.json", "w") as dic:
#     dic.write(param)

# bolt=json.dumps(bolt)
# with open("muvro/bolts.json", "w") as dic:
#     dic.write(bolt)

# pin=json.dumps(pin)
# with open("muvro/pin.json", "w") as dic:
#     dic.write(pin)

# pins=json.dumps(pins)
# with open("muvro/pinsparam.json", "w") as dic:
# dic.write(pins)


# img=cap.get_frame((680,500))

# cv2.circle(img,(333,221),90,(255,255,255),-1)
# a = cv2.selectROIs("select the area", img)


# print(a.tolist())

# for r in a:
#     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
