
import cv2
import os
import numpy as np
import json
from cam import camera_streams
cap = camera_streams(mode="Industrial")

def detectCircle(img, radius=30, minDist=200,
                 param1=50,
                 param2=70,
                 minRadius=10,
                 ):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blurred = cv2.medianBlur(gray, 5)  #
    gray=cv2.bilateralFilter(gray,10,50,50)#
    cv2.imshow("blr",gray)
    minDist = minDist
    param1 = param1
    param2 = param2
    minRadius = minRadius
    maxRadius = radius

    # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    Max = 0
    center = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            if Max < i[2]:
                Max = i[2]
                center = i
                cv2.circle(img, (center[0], center[1]), center[2]+67, (255,255, 255), -1)

                # cv2.circle(img, (center[0], center[1]), center[2], (0, 255, 0), 2)
                # cv2.namedWindow("multi_img", cv2.WINDOW_NORMAL)
                # cv2.imshow('multi_img',img)
#                     cv2.waitKey(0)
#                     cv2.destroyAllWindows()
        return img,1
    else:
        return img,0
    
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
bolt = [[314, 116, 26, 24], [342, 116, 29, 25], [374, 126, 26, 27], [399, 144, 23, 30], [418, 171, 21, 29], [430, 201, 16, 31], [431, 227, 14, 35], [415, 259, 18, 29], [396, 284, 20, 25], [367, 304, 25, 22], [335, 305, 29, 30], [305, 310, 28, 21], [273, 297, 28, 24], [250, 277, 26, 26], [236, 253, 23, 29], [230, 220, 20, 34], [232, 191, 20, 31], [241, 162, 20, 31], [261, 143, 24, 25], [283, 127, 29, 18]]
# param={"min1": 153, "max1": 219, "min2": 164, "max2": 223, "min3": 184, "max3": 255, "min4": 183, "max4": 259, "min5": 192, "max5": 252, "min6": 138, "max6": 245, "min7": 126, "max7": 237, "min8": 97, "max8": 230, "min9": 85, "max9": 252, "min10": 75, "max10": 210, "min11": 62, "max11": 187, "min12": 51, "max12": 209, "min13": 102, "max13": 253, "min14": 77, "max14": 245, "min15": 88, "max15": 238, "min16": 164, "max16": 256, "min17": 116, "max17": 240, "min18": 71, "max18": 217, "min19": 94, "max19": 256, "min20": 170, "max20": 286}
# param={'min1': 192, 'max1': 196, 'min2': 193, 'max2': 199, 'min3': 240, 'max3': 248, 'min4': 236, 'max4': 243, 'min5': 238, 'max5': 245, 'min6': 232, 'max6': 242, 'min7': 222, 'max7': 232, 'min8': 222, 'max8': 230, 'min9': 241, 'max9': 248, 'min10': 199, 'max10': 206, 'min11': 177, 'max11': 184, 'min12': 197, 'max12': 205, 'min13': 232, 'max13': 240, 'min14': 221, 'max14': 229, 'min15': 230, 'max15': 236, 'min16': 232, 'max16': 240, 'min17': 231, 'max17': 237, 'min18': 173, 'max18': 177, 'min19': 211, 'max19': 216, 'min20': 231, 'max20': 241}


param = {}
pins = {}
print(len(bolt))
pause = 0
# for i in good:
while (1):

    img1 = cap.get_frame((680, 500))

    # img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
 
    # img2 = img.copy()

    rois = []

    img2,_=detectCircle(img1.copy())
    if _==0:
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)[1]

    # thresh=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                              cv2.THRESH_BINARY,13,15)
    # thresh=cv2.dilate(thresh1,(3,3),iterations=2)
    cv2.imshow("thresh", thresh)
    # cv2.imshow("thresh", thresh1)


    k = cv2.waitKey(1)
    if k == ord('s'):
        pause = 1
        print("stop")
    if k == ord('p'):
        pause = 0
        print('play')
    if pause == 0:
        for r, j in zip(bolt, range(1, 21)):

            img1 = cv2.rectangle(img1, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), 255, 1)
            roi = thresh[int(r[1]):int(r[1]+r[3]),
                         int(r[0]):int(r[0]+r[2])]

            bl = cv2.medianBlur(roi, 9)
            cv2.imshow("blur",bl)
            roi = cv2.Canny(bl,120,189)

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


param=json.dumps(param)
with open("muvro/boltsparam.json", "w") as dic:
    dic.write(param)

bolt=json.dumps(bolt)
with open("muvro/bolts.json", "w") as dic:
    dic.write(bolt)




# img=cap.get_frame((680,500))

# a = cv2.selectROIs("select the area", img)


# print(a.tolist())

# for r in a:
#     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
