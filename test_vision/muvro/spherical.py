import cv2 
import os
import numpy as np
import json
from cam import camera_streams
cap=camera_streams(mode="Industrial")
def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #                 print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName
# good=image_loc("sona_data/side")
# good=image_loc("sona_data/wside_wiso")        
# img=cv2.imread(good[1])
img=frame=cap.get_frame((680,500))
# r=cv2.selectROI(img)
r=(383, 9, 32, 70)
print(r)
mi=0
mx=0
h=0
w=0
def sphericala(image):
    global r,mi,mx,h,w
    try:    img=cv2.imread(image)
    except:img=image
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray",gray)
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = gray[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    bl1=cv2.GaussianBlur(roi,(3,3),cv2.BORDER_DEFAULT)
    # bl=cv2.medianBlur(roi, 3)
    bl1[bl1>20]=255

    
    
    h,w=bl1.shape            
    
    n_black=np.count_nonzero(bl1==255)

    
    roi=cv2.resize(bl1,(400,400))

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

    cv2.imshow("bl1",bl1)

    # print(mi,mx)
# for i in good:
#     camplate(i)
#     if cv2.waitKey(1)==ord('q'):break

from camera import checkcamera
while True:
    frame=cap.get_frame((680,500))
    # _,_,frame=checkcamera(no=3)
   
    sphericala(frame)
    if cv2.waitKey(2)==ord('q'):break
cv2.destroyAllWindows()


print(mi,mx,h*w)

camplatethrust=[mi,mx]
spr=json.dumps(r)
with open("muvro/spherical.json", "w") as dic:
    dic.write(spr)

camplatethrust=json.dumps(camplatethrust)
with open("muvro/sphericalthrust.json", "w") as dic:
    dic.write(camplatethrust)
    