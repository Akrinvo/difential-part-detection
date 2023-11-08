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





def pred_pinmodel(image=None,model=None):
    out=0
    categories=['pin',"wpin"]
    pin=[[372, 156, 26, 22], [401, 218, 23, 26], [287, 270, 29, 24], [259, 203, 23, 27]]    
    
    
    try:    img1=cv2.imread(image)
    except:img1=image
    r=(231,123,217,202)
    # img1=cv2.resize(img,(680,500))
    img=img1.copy()
    rois=[]
    count=0
    for r,j in zip(pin,range(1,5)):
        img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
        roi = img1[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        roi=cv2.resize(roi,(32,32))
        
        
        X = roi[np.newaxis, ...]
        p=model.predict(X)
        pr = np.argmax(p, axis=1)[0]

        # print(j,"-------",p)

        if pr!=0:
            count+=1
            img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
            overlay = np.zeros_like(img)
            overlay[:] = (0, 0,255)
        else:
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
    # test=image_loc("sona_data/wbolt_wpin")
    # test=image_loc("sona_data/bolt_pin")
    from cam import camera_streams
    cap=camera_streams(mode="Industrial")
    model=keras.models.load_model('newbolt/pinsmodel.h5')


    # for i in test:
        
        
    #     # cv2.imshow("roiss",roiss)
        
    #     img,out=pred_bolts(i)
    #     cv2.imshow("image",img)
    #     if cv2.waitKey(800)==ord("q"):break
    import time
    while True:

        a=time.time()
        frame=cap.get_frame((680,500))
        img, out=pred_pinmodel(image=frame,model=model)
        print("time taking ",time.time()-a)
        cv2.imshow("img",img)
        cv2.imshow("fram",frame)

        if cv2.waitKey(10)==ord('q'):break
    cv2.destroyAllWindows()

