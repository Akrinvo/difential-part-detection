import cv2 
import os
import numpy as np
import json
# from cam import camera_streams
# cap=camera_streams(mode="Industrial")










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

good=image_loc("new_data/wpin_ori")
good=image_loc("new_data/bolt_pin")


pin=[[184, 163, 16, 14], [488, 171, 18, 12], [485, 345, 16, 13], [181, 338, 15, 11]]
# pin=[[180, 162, 16, 15], [494, 168, 19, 16], [490, 342, 20, 16], [173, 334, 17, 14]]
pin=[[171, 146, 44, 45], [475, 160, 35, 38], [468, 326, 38, 38], [174, 319, 35, 36]]

param={}
pins={}

for i in good:
    img1=cv2.imread(i)
    shv=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
    img=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    cv2.imshow("hsv",shv)
    img=cv2.resize(img,(680,500))
   
    rois=[]
    thresh=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    g=cv2.cvtColor(shv,cv2.COLOR_BGR2GRAY)

    hsvthresh=cv2.threshold(g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    cv2.imshow("thresh",thresh)
    
    for r,j in zip(pin,range(1,5)):
        
        img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
        roi = thresh[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        
        roi1 = img[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        roi=cv2.resize(roi,(61,61))
        bl=cv2.GaussianBlur(roi,(15,15),cv2.BORDER_DEFAULT)
        edge=cv2.Canny(bl,20,240)
        
        fi=np.array([[255,0,255],[255,0,255],[255,0,255]])//255
        fi=np.ones((3,))
        fi=np.diag(fi)
    
        con=cv2.filter2D(edge,-1,fi)
        cv2.imshow("con"+str(j),con)

        





        # pin_black=61*61-np.count_nonzero(roi == 255)
        pin_black=np.count_nonzero(roi == 255)
        if pin_black>10:
            if len(pins)<8:
                pins[f"min{j}"]=pin_black
                pins[f"max{j}"]=pin_black
            else:
                if pins[f"min{j}"]>pin_black:pins[f"min{j}"]=pin_black
                if pins[f"max{j}"]<pin_black:pins[f"max{j}"]=pin_black
            
        
        cv2.imshow("edge"+str(j),edge)

        cv2.imshow(str(j),roi)

    print(pins)

    cv2.imshow("image",img)
    if cv2.waitKey(100)==ord("q"):break
# while True:
#     frame=cap.get_frame((680,500))
#     cv2.imshow("img",img)
#     if cv2.waitKey(200)==ord('q'):break
cv2.destroyAllWindows()
print(param)

# img=cv2.imread(good[2])
# img=cv2.resize(img,(680,500))
# a = cv2.selectROIs("select the area", img)
# # print(r)

# # r=(75, 139, 393, 174)
# # img = img[int(r[1]):int(r[1]+r[3]), 
# #                       int(r[0]):int(r[0]+r[2])]


# print(a.tolist())



# {'min1': 1207, 'max1': 1949, 'min2': 1212, 'max2': 1956, 'min3': 672, 'max3': 1358, 'min4': 325, 'max4': 1167}