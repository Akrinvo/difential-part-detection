import cv2 
import os
import numpy as np
import json
from tensorflow import keras






def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #                 print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName





def pred_boltsmodel(image,model=None):
    out=0
    categories=['bolt',"wbolt"]
    bolt = [[314, 116, 26, 24], [342, 116, 29, 25], [374, 126, 26, 27], [401, 144, 23, 30], [420, 169, 21, 29], [433, 201, 16, 31], [433, 227, 16, 35], [415, 257, 22, 29], [396, 282, 23, 25], [369, 304, 25, 22], [335, 305, 29, 30], [305, 310, 28, 21], [273, 297, 28, 24], [250, 277, 26, 26], [236, 253, 23, 29], [230, 220, 20, 34], [232, 191, 20, 31], [241, 162, 20, 31], [261, 141, 24, 25], [283, 125, 29, 18]]
    
    try:    img1=cv2.imread(image)
    except:img1=image
    # r=(231,123,217,202)
    # img1=cv2.resize(img1,(680,500))
    img=img1.copy()
    rois=[]
    count=0
    for r,j in zip(bolt,range(1,21)):
        img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
        roi = img1[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        roi=cv2.resize(roi,(32,32))
        
        X = roi[np.newaxis, ...]
        p=model.predict(X)
        pr = np.argmax(p, axis=1)[0]


        if pr!=0:
            count+=1
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
            overlay = np.zeros_like(img)
            overlay[:] = (0, 0,255)
        if pr==0:
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,2)
            

        # if j==20:
        #     img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(255,0,255),1)
        #     print(n_white,n_black)
        
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
   
    img = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    return img,out


if __name__=="__main__":


    from cam import camera_streams
    cap=camera_streams(mode="Industrial")
    model=keras.models.load_model('newbolt/boltmodel(1).h5')
    # for i in test:
        
        
    #     # cv2.imshow("roiss",roiss)
        
    #     img,out=pred_bolts(i)
    #     cv2.imshow("image",img)
    #     if cv2.waitKey(800)==ord("q"):break

    while True:
        import time 
        a=time.time()
        frame=cap.get_frame((680,500))
        img, out=pred_boltsmodel(image=frame,model=model)
        print("time taking",time.time()-a)
        cv2.imshow("img",img)
        cv2.imshow("fram",frame)

        if cv2.waitKey(2)==ord('q'):break
    cv2.destroyAllWindows()

