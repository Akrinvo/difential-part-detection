import cv2
import os
try:from pypylon import pylon
except:
    os.system("pip3 install pypylon")
    from pypylon import pylon



def camera_opner(no=3):
    
    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices()

    imagelist=[]
    for device,i in zip(devices,range(len(devices))):
        # print(device)
        camera = pylon.InstantCamera()
        
        camera.Attach(tl_factory.CreateFirstDevice(device))
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        camera.Open()
        camera.StartGrabbing(2)
        grab = camera.RetrieveResult(2000, pylon.TimeoutHandling_Return)
        if grab.GrabSucceeded():
            image = converter.Convert(grab)
            im = image.GetArray()

            width = 680
            height = 500
            dim = (width, height)

            im = cv2.resize(im, dim, cv2.INTER_AREA)
     
            

            imagelist.append(im)
    if len(imagelist)==no:
        return imagelist

def checkcamera(no=3):
    images=camera_opner(no=no)
    while(images==None):
        print("PROBLEM IN OPNING CAMERA")
        images=camera_opner(no=no)
    return images

if __name__=="__main__":
    while(1):
        try:
            image=checkcamera(no=3)
            cv2.imshow("cam1",image[0])
            cv2.imshow("cam2",image[1])
            cv2.imshow("cam3",image[2])

            if cv2.waitKey(1)==ord("q"):
                break
        except:print("a")
    cv2.destroyAllWindows()

