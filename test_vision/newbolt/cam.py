from pypylon import pylon
import numpy as np
import cv2 as cv
import random

class camera_streams:
    capture = None
    mode = None
    IP = None
    path = None

    def __init__(self, mode, IP=None, path=None):
        self.IP = IP
        self.mode = mode
        self.path = path
        if mode == 'Industrial':

            self.capture = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.capture.Open()
            self.capture.ExposureTime.SetValue(50000)
            self.capture.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_RGB16packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_LsbAligned
            self.bgr_img = self.frame = np.ndarray(shape=(self.capture.Height.Value, self.capture.Width.Value, 3),
                                                   dtype=np.uint8)
        elif mode == "IP cam":
            self.capture = cv.VideoCapture(self.IP)
            if self.capture.isOpened():
                print("IP Camera Connected.")
            else:
                print("Please check the host address/network connectivity")

        elif mode == "fromfile":
            self.capture = cv.VideoCapture(self.path)
            if self.capture.isOpened():
                print("Video File Ready to Read.")
            else:
                print("Path may be incorrect. Please check again.")

        else:
            for cameraID in range(0, 200):
                print("Looking for open camera device.")
                self.capture = cv.VideoCapture(cameraID)
                if self.capture.isOpened():
                    print("Working camID: ", cameraID)
                    break
                if cameraID == 200:
                    print("No camera ID is found working")

    def get_frame(self, size):
        if self.mode == "Industrial":
            grabResult = self.capture.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                frame = np.ndarray(buffer=image.GetBuffer(), shape=(image.GetHeight(), image.GetWidth(), 3),
                                   dtype=np.uint16)
                self.bgr_img[:, :, 0] = frame[:, :, 2]
                self.bgr_img[:, :, 1] = frame[:, :, 1]
                self.bgr_img[:, :, 2] = frame[:, :, 0]
                # print(self.bgr_img.shape, "----")
                self.frame = self.bgr_img.copy()
                self.frame = cv.resize(self.frame, size)
            else:
                print("Error in frame grabbing.")
            grabResult.Release()
        else:
            ret, self.frame = self.capture.read()
            if ret:
                self.frame = cv.resize(self.frame, size)
            else:
                print("Error in frame grabbing.")
        return self.frame

    def __del__(self):
        self.capture.close()
if __name__=="__main__":
    cap=camera_streams(mode="Industrial")
    count=0
    # overlay=cv.imread("new_data/withmoving/image614.jpg") # vision station dwon camera
    # overlay=cv.imread("new_data/isoplate/image974002.jpg") #vision station side camera
    # overlay=cv.imread("new_data/wbolt_pin/image5204.jpg")  #vision station top camera
    # overlay=cv.imread("new_data/rwasher/image816.jpg") # sub station right camera
    # overlay=cv.imread("new_data/lwwasher/image4519.jpg") # sub station left camer
    while True:
        frame=cap.get_frame((680,500))
        # img = cv.addWeighted(frame, 1, overlay, 0.7, 0)
        # reversd = cv.addWeighted(overlay, 1, frame, 0.5, 0)

        # hsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        # cv.imshow("overlay",img)
        # cv.imshow("overlay image",overlay)
        # cv.imshow("overlay reverd",reversd)
        # cv.circle(frame,(333,221),90,(255,255,255),-1)

        cv.imshow("actual",frame)
        k=cv.waitKey(1)
        if k==ord("q"):
            break
    # if k==ord("s"):
        # cv.imwrite(f"muvro/sona_data/image{random.randint(0,999999)}.jpg",frame)
        count+=1

#####################################################
  
    # cv.imwrite("img.jpg",frame)


    # img = cv2.imread("img.jpg",0)
    # # img=img[:,:,2]
    # imag2=img.copy()
    # #Denoise for better results
    # from skimage.restoration import denoise_tv_chambolle
    # img = denoise_tv_chambolle(img, weight=0.1, eps=0.0002,max_num_iter=200)

    # # Apply multi-Otsu threshold 
    # thresholds = threshold_multiotsu(img, classes=4)

    # # Digitize (segment) original image into multiple classes.
    # #np.digitize assign values 0, 1, 2, 3, ... to pixels in each class.
    # regions = np.digitize(img, bins=thresholds)
    # plt.imshow(regions)
    # plt.show()

    # segm1 = (regions == 0)
    # segm2 = (regions == 1)
    # segm3 = (regions == 2)
    # segm4 = (regions == 3)

    # plt.imshow(segm1)
    # plt.show()


    # #We can use binary opening and closing operations to clean up. 
    # #Open takes care of isolated pixels within the window
    # #Closing takes care of isolated holes within the defined window

    # from scipy import ndimage as nd

    # segm1_opened = nd.binary_opening(segm1, np.ones((3,3)))
    # segm1_closed = nd.binary_closing(segm1_opened, np.ones((3,3)))

    # segm2_opened = nd.binary_opening(segm2, np.ones((3,3)))
    # segm2_closed = nd.binary_closing(segm2_opened, np.ones((3,3)))

    # segm3_opened = nd.binary_opening(segm3, np.ones((3,3)))
    # segm3_closed = nd.binary_closing(segm3_opened, np.ones((3,3)))

    # segm4_opened = nd.binary_opening(segm4, np.ones((3,3)))
    # segm4_closed = nd.binary_closing(segm4_opened, np.ones((3,3)))


    # print(len(segm1),len(segm2),len(segm3),len(segm4))
    # all_segments_cleaned = np.zeros((img.shape[0], img.shape[1], 3)) 
    # all_segments_cleaned[segm1_opened] = (1,0,0)
    # all_segments_cleaned[segm2_opened] = (0,1,0)
    # all_segments_cleaned[segm3_opened] = (0,0,1)
    # all_segments_cleaned[segm4_closed] = (1,1,0)


    # plt.imshow(all_segments_cleaned) 
    # plt.show()

    # imag2[segm1_closed]=0
    # kernel = np.ones((17,17),np.uint8)

    # # Convolve and Save Output
    # output = convolve2D(imag2, kernel, padding=3)
    # mul=imag2*output

    # cv2.imwrite("imggg.png",mul)
    # # plt.savefig("BSE_segmented.jpg",mul)

    # cv2.imshow("imagee1",mul)

    # cv2.imshow("imagee",imag2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
