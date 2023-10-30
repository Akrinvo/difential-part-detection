#CODE for finding out range of white pixels across images

import cv2
import os
import numpy as np
import json

def get_image_filenames(folder_path):
    filenames = []
    for root, dirs, files in os.walk(os.path.abspath(folder_path)):
        for filename in files:
            file_path = os.path.abspath(os.path.join(root, filename))
            filenames.append(file_path)
    return filenames

#jab side washer nhi hai
image_filenames = get_image_filenames("D:\\work1_main\\background2")
print("Total images:", len(image_filenames))

#ROI coordinates
img = cv2.imread(image_filenames[8])
# roi_coordinates = cv2.selectROI(img)
roi_coordinates = (565, 69, 56, 92)

print(roi_coordinates)

min_white_pixels = 0
max_white_pixels = 0

for image_filename in image_filenames:
    image = cv2.imread(image_filename)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Image", gray_image)
    

    roi_x, roi_y, roi_width, roi_height = roi_coordinates
    cv2.rectangle(image, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 255, 255), 1)

    
    roi = gray_image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    roi[roi > 130] = 0
    
    if np.sum(roi) != 0:
        # apply Canny edge detection
        roi = cv2.medianBlur(roi, 5)
        edge = cv2.Canny(roi, 30, 100)
        # sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize= 3)
        # sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        # magnitude = np.sqrt(sobel_x**2 + sobel_y**2)


        # apply thresholding
        roi_thresholded = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # roi_thresholded = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # dest = cv2.Laplacian(roi, cv2.CV_16S, ksize=3)
        # abs_dest = cv2.convertScaleAbs(dest)

        n_white_pixels = np.count_nonzero(edge == 255)
        edge = cv2.resize(edge, (400, 400))
        roi_thresholded = cv2.resize(roi_thresholded, (400, 400))
        # magnitude = cv2.resize(magnitude, (400, 400))
        # abs_dest = cv2.resize(edge, (400, 400))
        cv2.imshow("Thresholded ROI", roi_thresholded)
        # cv2.imshow("Magnitude", magnitude)
        cv2.imshow("Canny Edge Detection", edge)
        # cv2.imshow("Laplacian", abs_dest )
        
        if n_white_pixels > 100:
            if min_white_pixels == 0:
                min_white_pixels = n_white_pixels
            if max_white_pixels == 0:
                max_white_pixels = n_white_pixels
            if min_white_pixels > n_white_pixels:
                min_white_pixels = n_white_pixels
            if max_white_pixels < n_white_pixels:
                max_white_pixels = n_white_pixels
                
    cv2.imshow("Image with ROI Rectangle", image)
   
    if cv2.waitKey(20) == ord('q'):
        break

cv2.destroyAllWindows()

print("Min white pixels:", min_white_pixels)
print("Max white pixels:", max_white_pixels)


data ={
    "min_white_pixels": min_white_pixels,
    "max_white_pixels": max_white_pixels
}
json_filename = "range_bg.json"
with open(json_filename, "w") as json_file:
    json.dump(data, json_file)

print(f"Data saved to {json_filename}")


data_1 ={
    "roi_coordinates": roi_coordinates
}
json_filename_1 = "roi_bg.json"
with open(json_filename_1, "w") as json_file:
    json.dump(data_1, json_file)

print(f"ROI saved to {json_filename_1}")