import cv2 
import os
import numpy as np
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
good=image_loc("muvro_f_data/lbwasher")

img=cv2.imread(good[1])
r=cv2.selectROI(img)
r=(213, 247, 31, 20)
print(r)
mi=0
mx=0
def side_washer(image):
    global r,mi,mx
    try:    img=cv2.imread(image)
    except:img=image
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray",gray)
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = gray[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    roi[roi>130]=0
    if np.sum(roi)!=0:
        edge=cv2.Canny(roi,70,170)
        roi=cv2.threshold(roi,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        
        n_white=np.count_nonzero(roi == 255)
        edge=cv2.resize(edge,(400,400))
        
        roi=cv2.resize(roi,(400,400))
        if mi==0:
            mi=n_white
        if mx==0:
            mx=n_white
        if mi>n_white:
            mi=n_white
        if mx<n_white:
            mx=n_white
    cv2.imshow("img",img)
    cv2.imshow("roi",roi)
    cv2.imshow("edge",edge)

for i in good:
    side_washer(i)

    if cv2.waitKey(100)==ord('q'):break


while True:
    frame=cap.get_frame((680,500))
    side_washer(frame)
    if cv2.waitKey(200)==ord('q'):break
cv2.destroyAllWindows()
print(mi,mx)
    