import cv2
import numpy as np

img = cv2.imread("new_data/bolt_pin/image0.jpg")
pin=[[184, 163, 16, 14], [488, 171, 18, 12], [485, 345, 16, 13], [181, 338, 15, 11]]

# variables


point=[]
drawing = False
no=0
def draw_rectangle_with_drag(event, x, y, flags, param):
	
	global  drawing, roi,no,point
	
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		print(point)
		no+=1	
		point.append((x,y))	
			
	if no==3 and drawing==True:
		print("hh")
		cv2.line(roi, point[0],
						point[1],
						color =(0, 255, 255),
						thickness =1)
		no=0
		point=[]
		drawing=False
	
	
		
cv2.namedWindow(winname = "Title of Popup Window")
cv2.setMouseCallback("Title of Popup Window",
					draw_rectangle_with_drag)


for r,j in zip(pin,range(1,5)):
        
        # img=cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),255,1)
        roi = img[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        cv2.line(roi, (0,17),
						(34,23),
						color =(0, 255, 255),
						thickness =1)
        cv2.imshow("Title of Popup Window", roi)
		
        cv2.waitKey(0) 
		
cv2.destroyAllWindows()
