import cv2 
import os
import numpy as np
# from cam import camera_streams
# cap=camera_streams(mode="Industrial")
def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName
bad=image_loc("muvro_f_data/wlbwasher")


r=(213, 247, 31, 20)
mi=35
mx=604

def pred_sidewasher(image):
    out=0
    global mi,mx,r

    try: img=cv2.imread(image)
    except:img=image
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)

    roi = gray[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
    edge=cv2.Canny(roi,70,170)
    
    
    n_white=np.count_nonzero(edge == 255)
    
    edge=cv2.resize(edge,(400,400))
    if mi>n_white:
        img=cv2.putText(img,"OK",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        out=1
        overlay = np.zeros_like(img)
        overlay[:] = (0, 255,0)
                

    
    elif mx<n_white:
            img=cv2.putText(img,"OK",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
            out=1
            overlay = np.zeros_like(img)
            overlay[:] = (0, 255,0)
    
    

    else:
        img=cv2.putText(img,"Ng",(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),(0,0,255),3)
        overlay = np.zeros_like(img)
        overlay[:] = (0, 0,255)

    img = cv2.addWeighted(img, 1, overlay, 0.5, 0)
    print(out)
    return img,out

if __name__ == "__main__":

    for i in bad:
        img=pred_sidewasher(i)
        cv2.imshow("img",img)
        if cv2.waitKey(200)==ord('q'):break

    # while True:
    #     frame=cap.get_frame((680,500))
    #     img=pred_sidewasher(frame)
    #     cv2.imshow("img",img)
    #     if cv2.waitKey(200)==ord('q'):break
    cv2.destroyAllWindows()
    print(mi,mx)
        