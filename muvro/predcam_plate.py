import cv2 
import os
import numpy as np
import json
# from cam import camera_streams
# cap=camera_streams(mode="Industrial")

with open('./muvro/camplate.json', 'r') as openfile:
    r= json.load(openfile)

with open('./muvro/camplatethrust.json', 'r') as openfile:
    mi,mx= json.load(openfile)


def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #                 print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName


def pred_camplate(image):
    global mi,mx,r
    out=0
    try:    img=cv2.imread(image)
    except:img=image
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = gray[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    bl=cv2.medianBlur(roi,3)
    
    roi=cv2.threshold(bl,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    n_white=np.count_nonzero(roi == 255)
    
    roi=cv2.resize(roi,(400,400))
    # cv2.imshow("roi",roi)
    # print(n_white,mi)
    if mi-1500>n_white:
                img=cv2.putText(img,"NG",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
                img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
                overlay = np.zeros_like(img)
                overlay[:] = (0, 0,255)

    
    # elif mx<n_white:
    #             img=cv2.putText(img,"NG",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
    #             img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
    #             overlay = np.zeros_like(img)
    #             overlay[:] = (0, 0,255)


    else:
        img=cv2.putText(img,"OK",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        
        out=1
        overlay = np.zeros_like(img)
        overlay[:] = (0, 255,0)

    img = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    return img,out

if __name__=="__main__":
    # bad=image_loc("sona_data/wcamring")
    # bad=image_loc("sona_data/down")

    # for i in bad:
    #     img,out=pred_camplate(i)
    #     cv2.imshow("img",img)
    #     if cv2.waitKey(1)==ord('q'):break
    from camera import checkcamera
    while True:
        # frame=cap.get_frame((680,500))
        _,frame,_=checkcamera(no=3)
        # frame=cap.get_frame((680,500))
        img,out=pred_camplate(frame)
        cv2.imshow("img",img)
        if cv2.waitKey(2)==ord('q'):break
    cv2.destroyAllWindows()
    print(mi,mx)
    