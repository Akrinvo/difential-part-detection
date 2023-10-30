import cv2
import os
import numpy as np
import json
def get_image_filenames(folder_path):
    #get a list of image filenames in a specified folder
    filenames = []
    for root, dirs, files in os.walk(os.path.abspath(folder_path)):
        for filename in files:
            file_path = os.path.abspath(os.path.join(root, filename))
            filenames.append(file_path)
    return filenames
def load_thresholds_from_json(json_filename):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
        min_threshold = data["min_white_pixels"]
        max_threshold = data["max_white_pixels"]
    return min_threshold, max_threshold
thresholds_json_filename = "muvro/range_bg.json"
min_threshold, max_threshold = load_thresholds_from_json(thresholds_json_filename)
def load_roi_from_json(json_filename_1):
    with open(json_filename_1, 'r') as json_file:
        data = json.load(json_file)
        roi_coordinates = data["roi_coordinates"]
    return roi_coordinates
roi_json_filename = "muvro/roi_bg.json"
roi_coordinates = load_roi_from_json(roi_json_filename)
yes,no = 0,0
images = get_image_filenames(r"C:\Users\Aspagteq\Desktop\good_gear")
# images = get_image_filenames(r"C:\Users\Aspagteq\Desktop\spring")
# images = get_image_filenames("D:\work1_main\withwasher_or1")
#images = get_image_filenames("D:\work1_main\withoutwasher")
def process_image(image_path):
    global min_threshold, max_threshold, roi_coordinates, yes, no
    try:
        img = cv2.imread(image_path)
    except:
        img = img
    roi_x, roi_y, roi_width, roi_height = roi_coordinates
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_with_roi = cv2.rectangle(img, (roi_x, roi_y),
                                 (roi_x + roi_width, roi_y + roi_height),
                                 (255, 255, 255), 1)
    roi = gray[roi_y:roi_y + roi_height,
               roi_x:roi_x+ roi_width]
    roi = cv2.medianBlur(roi, 5)
    edge = cv2.Canny(roi, 30, 100)
    # dest = cv2.Laplacian(roi, cv2.CV_16S, ksize=3)
    # abs_dest = cv2.convertScaleAbs(dest)
    roi_thresholded = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # roi_thresholded = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    n_white_pixels = np.count_nonzero(edge== 255)
    edge = cv2.resize(edge, (400, 400))
    roi_thresholded = cv2.resize(roi_thresholded, (400,400))
    # abs_dest = cv2.resize(edge, (400, 400))
    cv2.imshow("Thresholded ROI", roi_thresholded)
    cv2.imshow("Canny Edge Detection", edge)
    # cv2.imshow("Laplacian", abs_dest )
    if min_threshold <= n_white_pixels <= max_threshold:
        img_with_status = cv2.putText(img_with_roi, "NG", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        overlay = np.zeros_like(img_with_status)
        overlay[:] = (0, 0, 255)
        yes+=1
    else:
        img_with_status = cv2.putText(img_with_roi, "OK", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
        img_with_status = cv2.rectangle(img_with_status, (roi_x, roi_y),
                                       (roi_x + roi_width, roi_y + roi_height),
                                       (0, 0, 255), 3)
        overlay = np.zeros_like(img_with_status)
        overlay[:] = (0, 255,0)
        no+=1
    img_with_overlay = cv2.addWeighted(img_with_status, 1, overlay, 0.5, 0)
    print(yes,no)
    return img_with_overlay
for image_path in images:
    img_processed = process_image(image_path)
    cv2.imshow("Processed Image", img_processed)
    if cv2.waitKey(20) == ord('q'):
        break
cv2.destroyAllWindows()