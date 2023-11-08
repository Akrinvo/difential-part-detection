import cv2 
import os
# import imutils 
import numpy as np
import json
from tensorflow import keras







def pred_sphericalmodel(image=None,model=None):
    out=0
    r=(283, 1, 76, 61)

    try:    img=cv2.imread(image)
    except:img=image
    img1=img.copy()
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = img1[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    
    
    roi=cv2.resize(roi,(64,64))
    X = roi[np.newaxis, ...]
    p=model.predict(X)
    pr = np.argmax(p, axis=1)[0]
    ws=np.array(p)[0][1]
    s=np.array(p)[0][0]
    if pr==0:
        img=cv2.putText(img,"OK",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        out=1
        overlay = np.zeros_like(img)
        overlay[:] = (0, 255,0)
    elif ws>0.80:
                img=cv2.putText(img,"NG",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
                img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
                overlay = np.zeros_like(img)
                overlay[:] = (0, 0,255)
    else:
                img=cv2.putText(img,"NG",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
                img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
                overlay = np.zeros_like(img)
                overlay[:] = (0, 0,255)


    
    

    

    img = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    return img,out

if __name__=="__main__":
    # bad=image_loc("sona_data/wside_wiso")
    # bad=image_loc("sona_data/side")
    # for i in bad:
    #     img,out=pred_spherical(i)
    #     cv2.imshow("img",img)
    #     if cv2.waitKey(200)==ord('q'):break
    from cam import camera_streams

    cap=camera_streams(mode="Industrial")
    model=keras.models.load_model('newbolt/sphericalmodel(1).h5')
    while True:
        frame=cap.get_frame((680,500))
        img,out=pred_sphericalmodel(image=frame,model=model)
        cv2.imshow("img",img)
        if cv2.waitKey(200)==ord('q'):break
    cv2.destroyAllWindows()
  
    