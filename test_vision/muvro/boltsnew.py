
import cv2
import os
import numpy as np
import json
from cam import camera_streams
cap = camera_streams(mode="Industrial")
prev_circle=[112, 100 , 27]#[339 ,223 , 27 ]

def detectCircle(img, radius=30, minDist=200,
                 param1=60,
                 param2=70,
                 minRadius=10,
                 ):
    global prev_circle
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
        print("circle",circles)
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            if Max < i[2]:
                Max = i[2]
                center=i
                prev_circle=center
                
#                     cv2.waitKey(0)
#                     cv2.destroyAllWindows()
    print(prev_circle)
    cv2.circle(img, (prev_circle[0]-2, prev_circle[1]), prev_circle[2]+69, (255,255, 255), -1)

    cv2.circle(img, (prev_circle[0], prev_circle[1]), prev_circle[2], (0, 255, 0), 2)
    cv2.namedWindow("multi_img", cv2.WINDOW_NORMAL)
    cv2.imshow('multi_img',img)
    return img,1

    
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
bolt = [[314, 116, 26, 24], [342, 116, 29, 25], 
        [374, 126, 26, 27], [399+2, 144, 23, 30], 
        [418+2, 171-2, 21, 29], [430+3, 201, 16, 31],
          [431+2, 227, 14+2, 35], [415, 259-2, 18+4, 29], 
          [396, 284-2, 20+3, 25], [367+2, 304, 25, 22], 
          [335, 305, 29, 30], [305, 310, 28, 21], 
          [273, 297, 28, 24], [250, 277, 26, 26], 
          [236, 253, 23, 29], [230, 220, 20, 34], 
          [232, 191, 20, 31], [241, 162, 20, 31], 
          [261, 143-2, 24, 25], [283, 127-2, 29, 18]]


param = {}
pins = {}
print(len(bolt))
pause = 0
# for i in good:
while (1):

    img1 = cap.get_frame((680, 500))
    img2=img1.copy()
    # img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
 
    # img2 = img.copy()

    rois = []
    r=(231, 123, 217, 202)
    roi_circle = img2[int(r[1]):int(r[1]+r[3]), 
                        int(r[0]):int(r[0]+r[2])]
    c_img2,_=detectCircle(roi_circle)
    img2[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]=c_img2

    # img2,_=detectCircle(img1.copy())
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

            bl = cv2.medianBlur(roi, 5)
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
        # print(param)
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
