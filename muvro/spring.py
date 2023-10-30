import cv2 
import os
import numpy as np
import json
# from cam import camera_streams
# cap=camera_streams(mode="Industrial")
def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #                 print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName
good=image_loc("sona_data/left_focus/spring")
# good=image_loc("sona_data/left_focus/sidewasher")


img=cv2.imread(good[6])
r=cv2.selectROI(img)
r=(554, 196, 96, 102)#(620, 232, 28, 52)
print(r)
mi=0
mx=0
h,w=0,0
def spring(image):
    global r,mi,mx,h,w
    try:    img=cv2.imread(image)
    except:img=image
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray",gray)
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = gray[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    # bl1=cv2.GaussianBlur(roi,(3,3),cv2.BORDER_DEFAULT)
    # bl=cv2.medianBlur(roi, 3)
    roi[roi<70 ]=0

    
    
    h,w=roi.shape            
    
    n_black=h*w-np.count_nonzero(roi > 0)

    
    roi=cv2.resize(roi,(400,400))

    if mi==0:
        mi=n_black
    if mx==0:
        mx=n_black
    if mi>n_black:
        mi=n_black
    if mx<n_black:
        mx=n_black
    cv2.imshow("img",img)


    cv2.imshow("roi",roi)

    # cv2.imshow("bl1",bl1)

    
for i in good:
    spring(i)
    if cv2.waitKey(10)==ord('q'):break


# while True:

#     frame=cap.get_frame((680,500))
#     spring(frame)

#     cv2.imshow("img",img)
#     if cv2.waitKey(200)==ord('q'):break


cv2.destroyAllWindows()
sprthresh=[mi,mx]
print(mi,mx,h*w)
spr=json.dumps(r)
with open("spring.json", "w") as dic:
    dic.write(spr)

sprthresh=json.dumps(sprthresh)
with open("sprthresh.json", "w") as dic:
    dic.write(sprthresh)
    