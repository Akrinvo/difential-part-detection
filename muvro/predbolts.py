import cv2 
import os
import numpy as np
import json
#from cam import camera_streams



with open('./muvro/bolts.json', 'r') as openfile:
    bolt= json.load(openfile)
with open('./muvro/boltsparam.json', 'r') as openfile:
    param= json.load(openfile)

with open('./muvro/pinsparam.json', 'r') as openfile:
    pins= json.load(openfile)

with open('./muvro/pin.json', 'r') as openfile:
    pin= json.load(openfile)

# a=[[322   ,8  ,62,  25], [393 , 13,  58  ,42], [469  ,42  ,45  ,52], [524  ,96  ,38  ,57],[560 ,160  ,33  ,60], [577 ,237  ,28  ,55],[552 ,309  ,36  ,54], [512 ,375  ,40  ,50], [459 ,432  ,40  ,37], [389 ,471  ,44 , 27], [305 ,486  ,65  ,14], [238 ,468  ,46  ,24], [173 ,424  ,42  ,34], [124 ,363  ,38  ,47], [ 94 ,296  ,30  ,47], [ 86 ,221  ,22 , 55], [101 ,155  ,35  ,45], [136 , 98  ,48  ,39], [190  ,39  ,47  ,49], [256  ,12 , 51  ,34]]

# param={'min1': 810, 'max1': 1550, 'min2': 1172, 'max2': 2436, 'min3': 1077, 'max3': 2340, 'min4': 1049, 'max4': 2166, 'min5': 976, 'max5': 1980, 'min6': 671, 'max6': 1540, 'min7': 1166, 'max7': 1944, 'min8': 1145, 'max8': 2000, 'min9': 952, 'max9': 1471, 'min10': 757, 'max10': 1188, 'min11': 486, 'max11': 910, 'min12': 705, 'max12': 1104, 'min13': 854, 'max13': 1428, 'min14': 967, 'max14': 1786, 'min15': 731, 'max15': 1410, 'min16': 554, 'max16': 1210, 'min17': 1082, 'max17': 1575, 'min18': 1075, 'max18': 1872, 'min19': 1206, 'max19': 2300, 'min20': 1040, 'max20': 1734}

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





def pred_bolts(image):
    out=0
    global bolt,param
    try:    img=cv2.imread(image)
    except:img=image
    img=cv2.resize(img,(680,500))
    grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    grey1=grey.copy()
    # cv2.circle(grey,(333,221),98,(255,255,255),-1)
    # img =imutils.rotate(img,270)
    thresh=cv2.threshold(grey1,80,255,cv2.THRESH_BINARY)[1]
    rois=[]
    count=0
    for r,j in zip(bolt,range(1,21)):
        img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
        roi = thresh[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        bl=cv2.medianBlur(roi, 9)
    
    
        roi=cv2.Canny(bl,100,180)
        rh,rw=roi.shape
        n_black=np.count_nonzero(roi == 255)
     
        
    
        if  abs(param[f"max{j}"]-n_black)<25:
            count+=1
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
            overlay = np.zeros_like(img)
            overlay[:] = (0, 0,255)
            print("max ",param[f"max{j}"],f"no {j} bolt ",n_black," diff =",abs(param[f"max{j}"]-n_black))
        # elif(param[f"min{j}"]>n_black):
        #     count+=1
        #     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
        #     overlay = np.zeros_like(img)
        #     overlay[:] = (0, 0,255)
        #     print("min ",param[f"min{j}"],f"{j} bolt ",n_black," diff ",param[f"min{j}"]-n_black+3)

        else:
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,2)
            

        # if j==20:
        #     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(255,0,255),1)
        #     print(n_white,n_black)
        rois.append(roi)
    img=cv2.putText(img,str(count),(img.shape[0]-1,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
    if count>0:
            img=cv2.putText(img,"NG",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
            # img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
            overlay = np.zeros_like(img)
            overlay[:] = (0, 0,255)
    else:
        img=cv2.putText(img,"OK",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,2)
        out=1
        overlay = np.zeros_like(img)
        overlay[:] = (0, 255,0)
    roiss=vconcat_resize([hconcat_resize(rois[:5]),hconcat_resize(rois[5:10]),hconcat_resize(rois[10:15]),hconcat_resize(rois[15:20])])
    roiss=cv2.resize(roiss,(400,400))
    img = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    # cv2.imshow("thresh",roiss)

    return img,out


if __name__=="__main__":
    # test=image_loc("sona_data/wbolt_wpin")
    # test=image_loc("sona_data/bolt_pin")


    # for i in test:
        
        
    #     # cv2.imshow("roiss",roiss)
        
    #     img,out=pred_bolts(i)
    #     cv2.imshow("image",img)
    #     if cv2.waitKey(800)==ord("q"):break
    from cam import camera_streams
    cap=camera_streams(mode="Industrial")
    while True:
        frame=cap.get_frame((680,500))
        img, out=pred_bolts(frame)
        cv2.imshow("img",img)
        cv2.imshow("fram",frame)

        if cv2.waitKey(2)==ord('q'):break
    cv2.destroyAllWindows()
    print(param)

# r = cv2.selectROIs("select the area", img)
# print(r)

# r=(75, 139, 393, 174)
# img = img[int(r[1]):int(r[1]+r[3]), 
#                       int(r[0]):int(r[0]+r[2])]







# a=[ [293, 151,  21 , 13],[322 ,141 , 26,  14], [356, 142,  23 , 17], [390, 152,  19,  19], [416, 174 , 20 , 22], [436, 202,  13  ,19], [445 ,232 , 15 , 24], [445, 265,  13 , 24], [431 ,298 , 13 , 18], [407, 325,  16,  15], [377 ,343,  19 , 14], [377, 343,  19,  14], [339 ,352,  26,  11], [305, 345 , 28 , 14], [279 ,334,  23,  14], [255 ,311 , 21 , 20], [238 ,282 , 21 , 28], [228 ,249 , 18 , 28], [232 ,216 , 18 , 25], [248, 188 , 15 , 24], [266 ,164 , 18 , 18]]
# for r in a:
#     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()