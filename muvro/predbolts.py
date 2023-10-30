import cv2 
import os
import numpy as np
import json




with open('./muvro/bolts.json', 'r') as openfile:
    bolt= json.load(openfile)
with open('./muvro/boltsparam.json', 'r') as openfile:
    param= json.load(openfile)



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
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName





def pred_bolts(image):
    out=0
    global bolt,param
    try:    img=cv2.imread(image)
    except:img=image
    # img=cv2.resize(img,(680,500))
    grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    grey1=grey.copy()
   
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
            # print("max ",param[f"max{j}"],f"no {j} bolt ",n_black," diff =",abs(param[f"max{j}"]-n_black))
        else:
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,2)
            
        rois.append(roi)
    img=cv2.putText(img,str(count),(img.shape[0]-1,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
    if count>0:
            img=cv2.putText(img,"NG",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
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
   

    return img,out


if __name__=="__main__":

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





