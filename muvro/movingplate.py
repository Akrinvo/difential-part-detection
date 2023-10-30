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
good=image_loc("sona_data/down")
# good=image_loc("sona_data/wmoving")
img=cap.get_frame((680,500))
# r=cv2.selectROI(img)
r=(7, 122, 150, 69)#(23, 135, 77, 75)
print(r)
mi=0
mx=0
def movingplate(image):
    global r,mi,mx
    try: img=cv2.imread(image)
    except:img=image
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = gray[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    edge=cv2.Canny(roi,90,250)
    roi=cv2.threshold(roi,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    n_white=np.count_nonzero(edge == 255)
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

# for i in good:
#     movingplate(i)

#     if cv2.waitKey(10)==ord('q'):break
while True:
    frame=cap.get_frame((680,500))
    movingplate(frame)
    if cv2.waitKey(2)==ord('q'):break

cv2.destroyAllWindows()

print(mi,mx)
movingplatethrust=[mi,mx]
spr=json.dumps(r)
with open("muvro/movingplate.json", "w") as dic:
    dic.write(spr)

movingplatethrust=json.dumps(movingplatethrust)
with open("muvro/movingplatethrust.json", "w") as dic:
    dic.write(movingplatethrust)