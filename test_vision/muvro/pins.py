import cv2 
import os
import numpy as np
import json
from cam import camera_streams
cap=camera_streams(mode="Industrial")



def hconcat_resize(img_list, 
                   interpolation 
                   = cv2.INTER_CUBIC):
      # take minimum hights
    h_min = min(img.shape[0] 
                for img in img_list)
      
    # image resizing 
    im_list_resize = [cv2.resize(img,
                       (int(img.shape[1] * h_min / img.shape[0]),
                        h_min), interpolation
                                 = interpolation) 
                      for img in img_list]
      
    # return final image
    return cv2.hconcat(im_list_resize)
  
#function is for concatinate the image vertically

def vconcat_resize(img_list, interpolation 
                   = cv2.INTER_CUBIC):
      # take minimum width
    w_min = min(img.shape[1] 
                for img in img_list)
      
    # resizing images
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation = interpolation)
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

good=image_loc("muvro/sona_data")
# # good=image_loc("sona_data/wbolt_wpin")


pin=[[263, 214, 13, 12], [374, 164, 15, 12], [404, 226, 13, 13], [292, 276, 13, 13]]



pins={}

pause=0
# for i in good:
while(1):
    # img1=cv2.imread(i)
    img1=cap.get_frame((680,500))
    shv=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
    img=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    
    
   
    rois=[]
    thresh=cv2.threshold(img,80,255,cv2.THRESH_BINARY)[1]
   

    hsvthresh=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    cv2.imshow("thresh",thresh)
    cv2.imshow("otsu",hsvthresh)
    k=cv2.waitKey(1)
    if k==ord('s'):
        pause=1
        print("stop")
    if k==ord('p'):
        pause=0
        print('play')
    if pause==0:
       
        for r,j in zip(pin,range(1,5)):
            
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
            roi = thresh[int(r[1]):int(r[1]+r[3]), 
                        int(r[0]):int(r[0]+r[2])]
            croi = hsvthresh[int(r[1]):int(r[1]+r[3]), 
                    int(r[0]):int(r[0]+r[2])]

            roi=cv2.resize(roi,(61,61))
            edge=cv2.Canny(roi,170,200)
            # pin_black=61*61-np.count_nonzero(roi == 255)
            pin_black=np.count_nonzero(roi == 255)
            
            if len(pins)<8:
                pins[f"min{j}"]=pin_black
                pins[f"max{j}"]=pin_black
            else:
                if pins[f"min{j}"]>pin_black:pins[f"min{j}"]=pin_black
                if pins[f"max{j}"]<pin_black:pins[f"max{j}"]=pin_black
                
            
            # cv2.imshow("edge"+str(j),edge)
            cv2.imshow(str(j),roi)
        print(pins)
        cv2.imshow("image",img)
    if k ==ord("q"):break
# while True:
#     frame=cap.get_frame((680,500))
#     cv2.imshow("img",img)
#     if cv2.waitKey(200)==ord('q'):break
cv2.destroyAllWindows()





# pin=json.dumps(pin)s
# with open("muvro/pin.json", "w") as dic:
#     dic.write(pin)

# pins=json.dumps(pins)
# with open("muvro/pinsparam.json", "w") as dic:
#     dic.write(pins)



# {'min1': 2075, 'max1': 2766, 'min2': 3003,
#  'max2': 3721, 'min3': 3402, 'max3': 3721, 
# 'min4': 2464, 'max4': 3721}







# img=cap.get_frame((680,500))


# a = cv2.selectROIs("select the area", img)
# # print(r)

# # r=(75, 139, 393, 174)
# # img = img[int(r[1]):int(r[1]+r[3]), 
# #                       int(r[0]):int(r[0]+r[2])]


# print(a.tolist())

# # a=[[329, 111, 20, 11], [390, 133, 14, 20], [407, 158, 16, 21], [424, 186, 11, 21], [428, 215, 9, 26], [415, 245, 14, 20], [397, 274, 15, 16], [370, 293, 22, 15], [346, 307, 17, 9], [308, 309, 25, 9], [282, 304, 18, 11], [256, 283, 17, 16], [237, 263, 15, 13], [224, 229, 9, 21], [221, 196, 9, 24], [228, 170, 19, 13], [245, 145, 15, 18], [267, 127, 19, 9], [296, 114, 23, 10], [296, 114, 23, 10]]
# for r in a:
#     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

