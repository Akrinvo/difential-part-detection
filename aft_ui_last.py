import cv2
import os
import json
import threading
import time
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

from muvro.predcam_plate import*
from muvro.predmoving_plate import*
from muvro.pred_isoplate import*
from muvro.predbolts import*
from muvro.pred_spherical1 import*
from muvro.predpin import *

from tkinter import messagebox 
from muvro.camera import checkcamera

NO_OF_COMPONENTS = 6

cap = cv2.VideoCapture("first.avi")
cap1 = cv2.VideoCapture("sec.avi")
cap2 = cv2.VideoCapture("bolts.avi")
#=========================server==========================================
# import socket

# server_ip = "192.168.1.181"
# port = 5001

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP CONNECTION

# server_socket.bind((server_ip, port))

# server_socket.listen()

# client_socket, client_address = server_socket.accept()




#===================================================================

# ================================================================ =====================================================================================
root = Tk()
main_frame1 = LabelFrame(root)
processed_frame = LabelFrame(main_frame1)
processed_img_lbl = None
main_frame = LabelFrame(root)
cam_plate_frame = LabelFrame(main_frame)
cam_img_lbl = None
raw_frame = LabelFrame(main_frame)
moving_plate_frame = LabelFrame(main_frame)
moving_img_lbl = None
D_shape_frame = LabelFrame(main_frame)
no_b = None
work = None
spherical_washer_frame = LabelFrame(main_frame)
isolated_washer_frame = LabelFrame(main_frame)
bolts_frame = LabelFrame(main_frame)
processed_img_lbl = None
d_img_lbl = None
main_frame.pack()

cam_plate_yes, cam_plate_no = 0, 0
moving_plate_yes, moving_plate_no = 0, 0
isolated_yes, isolated_no = 0, 0
spherical_yes = 0
spherical_no = 0
bolt_yes, bolt_no = 0, 0
shape_y,shape_n = 0,0

counter = 0
count = 0
sub_counter=0

terminate = False
terminate3 = False
terminate1 = False
terminate2 = False
terminate4=False
terminate5 = False
lock = threading.Lock()

# ------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- load img ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------

def load_image(path, width, height):
    try:
        image = Image.open(path)
        image = image.resize((width,height))  # Resize the image if needed
        image_tk = ImageTk.PhotoImage(image)
        return image_tk
    except:
        return print("not working")

# --------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------  folder path ----------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

def image_loc(foldername):
    # extractte file
    fileName = []
    for root, dirs, files in os.walk(os.path.abspath(foldername)):
        for namef in files:
            #                 print(os.path.abspath(os.path.join(root, namef)))
            file_name = os.path.abspath(os.path.join(root, namef))
            fileName.append(file_name)
    return fileName


# ----------------------------------------------------- arrow code function----------------------------------------------------------

def draw_forward_arrow(canvas):
    '''

    :param canvas:
    :return:
    '''
    # Clear any existing drawings
    canvas.delete("all")

    # Define arrow points
    arrow_points = [(5, 10), (25, 10), (25, 5), (35, 12), (25, 20), (25, 15), (5, 15)]

    # Draw the arrow
    canvas.create_polygon(arrow_points, fill="blue", outline="black")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------  Cam plate Backened  ------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


def cam_plate_detection_ui(image_path, cam_plate_frame, raw_frame):
    global cam_plate_yes,cam_plate_no, cam_img_lbl, terminate, raw_cam_img_lbl, processed_img_lbl,sub_counter,counter
   
    # try:
    #     # print(img_path)
    #     img = cv2.imread(image_path)
    # if image_path is None:
    #     print("gsajgdasjdg")
    # else:
    try:
    # except:
        img = image_path

        im , out = pred_camplate(img.copy())

        filename = f"muvro/result/cam_plate.jpg"
        cv2.imwrite(filename, img)

        img_tk = load_image(filename,150,150)
        if cam_img_lbl:
            cam_img_lbl.destroy()
        cam_img_lbl = Label(cam_plate_frame,image=img_tk)
        cam_img_lbl.image = img_tk
        cam_img_lbl.pack()


        img_tk1 = load_image(filename,150,150)
        if raw_cam_img_lbl:
            raw_cam_img_lbl.destroy()
        raw_cam_img_lbl = Label(raw_frame,image=img_tk1)
        raw_cam_img_lbl.image = img_tk1
        raw_cam_img_lbl.pack()

        if out == 0:
            cam_plate_frame.configure(bg="red")
            cam_plate_no += 1
        else:
            cam_plate_frame.configure(bg="green")
            cam_plate_yes += 1
            terminate = True
            sub_counter+=1
            # work.config(text="Cam plate detected ....", bg="green")


        print(counter,sub_counter)
        if sub_counter==4:
            counter+=1
            sub_counter=0
        no_b.config(text=f"Counter : {counter}")

        y_cam_plate.config(text=f'No. of detected cam plate: {cam_plate_yes}')
        no_cam_plate.config(text=f'No. of not detected cam plate: {cam_plate_no}')
    except Exception as e:
        print(e)
        print("no img")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------  Moving Plate Backened  ------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def moving_plate_detection_ui(frame, moving_plate_frame, raw_frame):
    global moving_plate_no, moving_plate_yes, moving_img_lbl, terminate3, raw_moving_img_lbl, processed_img_lbl,sub_counter,counter
    # print(image_path)
    # try:
    #     # img = cv2.imread(image_path)
    # except:
    try:
        img = frame

        im , out = pred_moving_plate(img.copy())

        filename = f"muvro/result/moving_plate.jpg"
        cv2.imwrite(filename, img)

        img_tk = load_image(filename,150,150)
        if moving_img_lbl:
            moving_img_lbl.destroy()
        moving_img_lbl = Label(moving_plate_frame,image=img_tk)
        moving_img_lbl.image = img_tk
        moving_img_lbl.pack()


        img_tk1 = load_image(filename,150,150)
        if raw_moving_img_lbl:
            raw_moving_img_lbl.destroy()
        raw_moving_img_lbl = Label(raw_frame,image=img_tk1)
        raw_moving_img_lbl.image = img_tk1
        raw_moving_img_lbl.pack()

        if out == 0:
            moving_plate_frame.configure(bg="red")
            # raw_frame.configure(bg="red")
            moving_plate_no += 1
            # work.config(text="Moving plate detecting ....", bg="red")
        else:
            moving_plate_frame.configure(bg="green")
            # raw_frame.configure(bg="green")
            moving_plate_yes += 1
            terminate3 = True
            sub_counter+=1
            # work.config(text="Moving plate detected ....", bg="green")


        print(counter,sub_counter)
        if sub_counter==4:
            counter+=1
            sub_counter=0
        no_b.config(text=f"Counter : {counter}")

        y_moving_plate.config(text=f'No. of detected Pin Returning Plate: {moving_plate_yes}')
        no_moving_plate.config(text=f'No. of not detected Pin Returning Plate: {moving_plate_no}')
    except Exception as e:
        print(e)
        print("no img")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------  Isolated Plate Backened  ------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def isolated_washer_detection_ui(image_path, isolated_washer_frame, raw_frame):
    global isolated_img_lbl , isolated_no, isolated_yes, terminate1, raw_isolated_img_lbl, processed_img_lbl,sub_counter,counter
    # try:
    #     img = cv2.imread(image_path)
    # except:
    try:
        img = image_path

        im , out = pred_isoplate(img.copy())

        filename = f"muvro/result/isolated_plate.jpg"
        cv2.imwrite(filename, img)

        img_tk = load_image(filename,150,150)
        if isolated_img_lbl:
            isolated_img_lbl.destroy()
        isolated_img_lbl = Label(isolated_washer_frame,image=img_tk)
        isolated_img_lbl.image = img_tk
        isolated_img_lbl.pack()

        img_tk1 = load_image(filename,150,150)
        if raw_isolated_img_lbl:
            raw_isolated_img_lbl.destroy()
        raw_isolated_img_lbl = Label(raw_frame,image=img_tk1)
        raw_isolated_img_lbl.image = img_tk1
        raw_isolated_img_lbl.pack()

        if out == 0:
            isolated_washer_frame.configure(bg="red")
            isolated_no += 1
            # work.config(text="Isolated Washer detecting ....", bg="red")
        else:
            isolated_washer_frame.configure(bg="green")
            # work.config(text="Isolated Washer detected....", bg="green")
            isolated_yes += 1
            terminate1 = True
            sub_counter+=1

        print(counter,sub_counter)
        if sub_counter==4:
            counter+=1
            sub_counter=0
            
        no_b.config(text=f"Counter : {counter}")
        

        y_isolated_plate.config(text=f'No. of detected isolated Plate: {isolated_yes}')
        no_isolated_plate.config(text=f'No. of not detected isolated Plate: {isolated_no}')
    except Exception as e:
        print(e)
        print("no img")

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------  Spherical Washer Backened  ------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


def spherical_washer_detection_ui(image, spherical_washer_frame, raw_frame):
    global spherical_no, spherical_yes, sph_img_lbl, terminate2, raw_sph_img_lbl, processed_img_lbl,sub_counter,counter

    # try:
    #     img = cv2.imread(image)
    # except:
    try:
        img = image
        
        im , out = pred_spherical1(img.copy())
        print(out)

        filename = f"muvro/result/spherical_washer.jpg"
        cv2.imwrite(filename, img)

        img_tk = load_image(filename, 150, 150)
        if sph_img_lbl:
            sph_img_lbl.destroy()
        sph_img_lbl = Label(spherical_washer_frame, image=img_tk)
        sph_img_lbl.image = img_tk
        sph_img_lbl.pack()

        img_tk1 = load_image(filename,150,150)
        if raw_sph_img_lbl:
            raw_sph_img_lbl.destroy()
        raw_sph_img_lbl = Label(raw_frame,image=img_tk1)
        raw_sph_img_lbl.image = img_tk1
        raw_sph_img_lbl.pack()


        if out == 0:
            spherical_washer_frame.configure(bg="red")
            
            spherical_no += 1
            # work.config(text="Spherical Washer detecting....", bg="red")
            
        else:
            spherical_washer_frame.configure(bg="green")
            # work.config(text="Spherical Washer detected....", bg="green")

            spherical_yes += 1
            terminate2 = True
            sub_counter+=1
        print(counter,sub_counter)
        if sub_counter==4:
            counter+=1
            sub_counter=0
        

        y_spherical_washer.config(text=f'No. of detected spherical washer: {spherical_yes}')
        no_spherical_washer.config(text=f'No. of not detected spherical washer: {spherical_no}')
        no_b.config(text=f"Counter : {counter}")
    except Exception as e:
        print(e)
        print("no img")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------  Bolts Backened  ------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def bolts_detection_ui(image_path, bolt_frame, raw_frame):
    global bolt_img_lbl , bolt_no, bolt_yes, terminate4, raw_bolt_img_lbl, processed_img_lbl,sub_counter,counter

    # try:
    #     img = cv2.imread(image_path)
    # except:
    try:
        img = image_path

        im , out = pred_bolts(img.copy())

        filename = f"muvro/result/bolts.jpg"
        cv2.imwrite(filename, img)

        img_tk = load_image(filename,150,150)
        if bolt_img_lbl:
            bolt_img_lbl.destroy()
        bolt_img_lbl = Label(bolt_frame,image=img_tk)
        bolt_img_lbl.image = img_tk
        bolt_img_lbl.pack()

        img_tk1 = load_image(filename,150,150)
        if raw_bolt_img_lbl:
            raw_bolt_img_lbl.destroy()
        raw_bolt_img_lbl = Label(raw_frame,image=img_tk1)
        raw_bolt_img_lbl.image = img_tk1
        raw_bolt_img_lbl.pack()

        if out == 0:
            bolt_frame.configure(bg="red")
            # work.config(text="Bolts detecting ....", bg="red")
            bolt_no += 1
        else:
            bolt_frame.configure(bg="green")
            # work.config(text="Bolts detected....", bg="green")
            bolt_yes += 1
            sub_counter+=1
            terminate4 = True
        if sub_counter==4:
            counter+=1
            sub_counter=0
            
        print(counter,sub_counter)
        y_bolts.config(text=f'No. of detected Bolts: {bolt_yes}')
        no_bolts.config(text=f'No. of not detected Bolts: {bolt_no}')
        no_b.config(text=f"Counter : {counter}")
    except Exception as e:
        print(e)
        print("no img")


# ==========================================================================================================================================================
# ================================================== D-Pin Work ============================================================================================
# =========================================================================================================================================================

def pin_detection_ui(image_path, pin_frame, raw_frame):
    global d_img_lbl , shape_n,shape_y, terminate5, raw_d_img_lbl, processed_img_lbl,sub_counter,counter

    # try:
    #     img = cv2.imread(image_path)
    # except:
    try:
        img = image_path

        im , out = pred_pins(img.copy())

        filename = f"muvro/result/dpin.jpg"
        cv2.imwrite(filename, img)

        img_tk = load_image(filename,150,150)
        if d_img_lbl:
            d_img_lbl.destroy()
        d_img_lbl = Label(pin_frame,image=img_tk)
        d_img_lbl.image = img_tk
        d_img_lbl.pack()

        # filename1 = f"result/raw_plate.jpg"
        # cv2.imwrite(filename1, img)
        img_tk1 = load_image(filename,150,150)
        if raw_d_img_lbl:
            raw_d_img_lbl.destroy()
        raw_d_img_lbl = Label(raw_frame,image=img_tk1)
        raw_d_img_lbl.image = img_tk1
        raw_d_img_lbl.pack()

        if out == 0:
            pin_frame.configure(bg="red")
            time.sleep(0.15)

            # work.config(text="Pin detecting....", bg="red")
            shape_n += 1
        else:
            pin_frame.configure(bg="green")
            # work.config(text="All detection Completed....", bg="green")
            shape_y += 1
            sub_counter+=1
            time.sleep(0.15)

            terminate5 = True
        if sub_counter==4:
            counter+=1
            sub_counter=0
            pin_frame.configure(bg="white")
        print(counter,sub_counter)
        y_D_shape.config(text=f'No. of detected pins: {shape_y}')
        no_D_shape.config(text=f'No. of not detected pins: {shape_n}')
        no_b.config(text=f"Counter : {counter}")
    except Exception as e:
        print(e)
        print("no img")

# ------------------------------------------------------- Connectivity ----------------------------------------------

def check_components():
    global client_socket
    while True:
        # recieved_data = client_socket.recv(1024).decode()
        # print("Recieved Data : ",recieved_data)
        # trigger=recieved_data.replace("}","").replace("{",'').split(":")[-1]
        trigger='1'
        if eval(trigger)==1:
            # reset the UI and update counter
            ##
            isolated_washer_frame.configure(bg="white")
            spherical_washer_frame.configure(bg="white")
            cam_plate_frame.configure(bg="white")
            bolts_frame.configure(bg="white")
            moving_plate_frame.configure(bg="white")
            D_shape_frame.configure(bg="white")
            ##
                
            for loop in range(3):          
            
                # first cam:

                try:
                    topCamera,downCamera=checkcamera(no=2)
                    sideCamera=downCamera
                    # print(topCamera, sideCamera, downCamera)
                    if topCamera is None:
                        work.config(text="Camera3 is not working")
                        icon_img = cv2.imread("images/logo.jpg")
                        topCamera,sideCamera,downCamera = icon_img,icon_img,icon_img
                    elif sideCamera is None:
                        work.config(text="Camera3 is not working")
                        icon_img = cv2.imread("images/logo.jpg")
                        topCamera,sideCamera,downCamera = icon_img,icon_img,icon_img
                    elif downCamera is None:
                        work.config(text="Camera3 is not working")
                        icon_img = cv2.imread("images/logo.jpg")
                        topCamera,sideCamera,downCamera = icon_img,icon_img,icon_img

                except Exception as e:
                    print(e) 
                    work.config(text="Camera3 is not working")
                    icon_img = cv2.imread("images/logo.jpg")
                    topCamera,sideCamera,downCamera = icon_img,icon_img,icon_img
                    
                cam_plate_detection_ui(downCamera,cam_plate_frame,raw_cam_plate_frame)
                moving_plate_detection_ui(downCamera,moving_plate_frame,raw_moving_plate_frame)
            
            # second cam:


            
                isolated_washer_detection_ui(sideCamera,isolated_washer_frame,raw_isolated_washer_frame)
                spherical_washer_detection_ui(sideCamera,spherical_washer_frame,raw_spherical_washer_frame)
            
            # Third cam:
        

            
                bolts_detection_ui(topCamera,bolts_frame,raw_bolts_frame)
                pin_detection_ui(topCamera,D_shape_frame,raw_D_shape_frame)
            

    











    ###########################################################################################################
            #     try:
            #         ret1, frame_from_cam = cap.read()
            #     except Exception as e:
            #         print("cam3 is not working")
            #         print(e)
            #         icon = cv2.imread("images/logo.jpeg")
            #         print(icon)
            #         frame_from_cam = icon
            #         work.config(text="Camera3 is not working")

            #     cam_plate_detection_ui(frame_from_cam,cam_plate_frame,raw_cam_plate_frame)
            #     moving_plate_detection_ui(frame_from_cam,moving_plate_frame,raw_moving_plate_frame)
            # # except:
            #     # print("cam1 not working")
            #     # work.config(text="Camera1 is not working")

            # # second cam:
            # # requires camera cap object for the respective camera

            # # try:

            #     # ret2, frame_from_cam1 = cap1.read()
            #     isolated_washer_detection_ui(frame_from_cam,isolated_washer_frame,raw_isolated_washer_frame)
            #     spherical_washer_detection_ui(frame_from_cam,spherical_washer_frame,raw_spherical_washer_frame)
            # # except:
            # #     print("cam2 is not working")
            # #     work.config(text="Camera2 is not working")
            # # Third cam:
            # # requires camera cap object for the respective camera

            # # try:
            #     # ret3, frame_from_cam2 = cap2.read()
            #     bolts_detection_ui(frame_from_cam,bolts_frame,raw_bolts_frame)
            #     pin_detection_ui(frame_from_cam,D_shape_frame,raw_D_shape_frame)
            

    #########################################################################################################################
                # trigger = False

                # give signal to port depending on sub - counter
                if sub_counter==NO_OF_COMPONENTS:
                    #signal is 1 (good)
                    pass
                else:
                    #signal is 0 (bad)
                    pass
            global shape_y, spherical_yes, bolt_yes, isolated_yes, cam_plate_yes, moving_plate_yes
            
            if shape_y > 1:
                Pin = 1
                shape_y = 0
            else:
                shape_y = 0
                Pin = 2

            if spherical_yes > 1:
                Spherical = 1
                spherical_yes = 0
            else:
                spherical_yes = 0
                Spherical = 2

            if bolt_yes > 1:
                Bolt = 1
                bolt_yes = 0
            else:
                bolt_yes = 0
                Bolt = 2

            if isolated_yes > 1:
                Isolated = 1
                isolated_yes = 0
            else:
                isolated_yes = 0
                Isolated = 2

            if cam_plate_yes > 1:
                Camplate = 1
                cam_plate_yes = 0
            else:
                cam_plate_yes = 0
                Camplate = 2

            if moving_plate_yes > 1:
                Moving = 1
                moving_plate_yes = 0
            else:
                moving_plate_yes = 0
                Moving = 2

            # Send data to remote
            # SIGNAL_DICT = {"VI_20_BOLT_CHECK": Bolt,
            #                "VI_ISOLATING_PLATE_CHECK": Isolated,
            #                "VI_PIN_CHECK": Pin,
            #                "VI_CAM_PLALE_CHECK": Camplate,
            #                "VI_RETURNING_PLATE_CHECK": Moving,
            #                "VI_FLATE_WASHER_CHECK": Spherical}
            # client_socket.sendall(str(SIGNAL_DICT).encode())
        else:
            # No trigger
            pass
# ===============================================================================================================================================================
# ===============================================================================================================================================================

bg_color = "mint cream"
root.title("Interface")
root.geometry("1295x700+0+0")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------- section 1 starts here -----------------------------------------------

heading = Label(root, text="After Assembly", font=("times new roman", 30, "bold"), bg=bg_color,
                fg="black", relief=GROOVE)

image_tk = load_image("muvro/images/logo.jpeg",100,50)
image_label2 = Label(heading, image=image_tk)
image_label2.image = image_tk  # Store a reference to the image to prevent garbage collection
image_label2.pack(side=LEFT)

heading.pack(fill=X)

# =================================================== Section 2 stars here ====================================================================

main_frame1 = LabelFrame(root, text="" , font=("times of roman", 5, "bold"), fg="black", relief=GROOVE, bg=bg_color, padx=5, pady=1)
# main_frame1.pack(fill=X)
main_frame1.pack(fill=BOTH,expand=True)

main_frame1.columnconfigure(0,weight=1)
main_frame1.columnconfigure(1,weight=1)
main_frame1.columnconfigure(2,weight=1)
main_frame1.columnconfigure(3,weight=1)
main_frame1.columnconfigure(4,weight=1)
main_frame1.columnconfigure(5,weight=1)
main_frame1.columnconfigure(6,weight=1)
# main_frame.columnconfigure(7,weight=1)
# main_frame.columnconfigure(8,weight=1)
# main_frame.columnconfigure(9,weight=1)
# main_frame.columnconfigure(10,weight=1)

main_frame1.rowconfigure(0,weight=1)
main_frame1.rowconfigure(1,weight=1)
main_frame1.rowconfigure(2,weight=1)
main_frame1.rowconfigure(3,weight=1)
main_frame1.rowconfigure(4,weight=1)
main_frame1.rowconfigure(5,weight=1)
main_frame1.rowconfigure(6,weight=1)
# main_frame.rowconfigure(7,weight=1)
# main_frame.rowconfigure(8,weight=1)
# main_frame.rowconfigure(9,weight=1)
# main_frame.rowconfigure(10,weight=1)

# raw cam plate  Label frame
raw_cam_plate_frame = LabelFrame(main_frame1, text="Raw Cam Plate", font=("times new roman", 15, "bold"), padx=10, pady=10)
raw_cam_plate_frame.grid(row=1, column=0, padx=5, pady=5)

# raw cam plate image frontend
image_tk1 = load_image("muvro/images/cam_plate.jpg",150,150)
raw_cam_img_lbl = Label(raw_cam_plate_frame, image=image_tk1)
raw_cam_img_lbl.image = image_tk1  # Store a reference to the image to prevent garbage collection
raw_cam_img_lbl.pack()

# raw Pin Returning Plate  Label frame
raw_moving_plate_frame = LabelFrame(main_frame1, text="Raw Pin Returning Plate",font=("times new roman", 15, "bold"), padx=10, pady=10)
raw_moving_plate_frame.grid(row=1, column=1, padx=5, pady=5)

# raw Pin Returning Plate image frontend
image_tk1 = load_image("muvro/images/cam_plate.jpg",150,150)
raw_moving_img_lbl = Label(raw_moving_plate_frame, image=image_tk1)
raw_moving_img_lbl.image = image_tk1  # Store a reference to the image to prevent garbage collection
raw_moving_img_lbl.pack()

# raw isolated washer label frame
raw_isolated_washer_frame = LabelFrame(main_frame1, font=("times new roman", 15, "bold"), text="Raw Isolated Plate", padx=10, pady=10)
raw_isolated_washer_frame.grid(row=1, column=2, padx=5, pady=5)

# raw isolated washer image frontend
image_tk6 = load_image("muvro/images/spherical_washer.jpg",150,150)
raw_isolated_img_lbl = Label(raw_isolated_washer_frame, image=image_tk6)
raw_isolated_img_lbl.image = image_tk6  # Store a reference to the image to prevent garbage collection
raw_isolated_img_lbl.pack()

# raw spherical washer label frame
raw_spherical_washer_frame = LabelFrame(main_frame1, font=("times new roman", 15, "bold"), text="Raw Flat Washer", padx=10, pady=10)
raw_spherical_washer_frame.grid(row=1, column=3, padx=5, pady=5)

# raw spherical washer image frontend
image_tk6 = load_image("muvro/images/spherical_washer.jpg",150,150)
raw_sph_img_lbl = Label(raw_spherical_washer_frame, image=image_tk6)
raw_sph_img_lbl.image = image_tk6  # Store a reference to the image to prevent garbage collection
raw_sph_img_lbl.pack()

# raw bolts label frame
raw_bolts_frame = LabelFrame(main_frame1,font=("times new roman", 15, "bold"), text="Raw Bolts", padx=10, pady=10)
raw_bolts_frame.grid(row=1, column=4, padx=5, pady=5,sticky="WENS")

# raw bolts image frontend
image_tk7 = load_image("muvro/images/bolts.jpeg",150,150)
raw_bolt_img_lbl = Label(raw_bolts_frame, image=image_tk7)
raw_bolt_img_lbl.image = image_tk7
raw_bolt_img_lbl.pack()

# raw D shape orientation label frame
raw_D_shape_frame = LabelFrame(main_frame1, text="Pin",font=("times new roman", 15, "bold"), padx=10, pady=10)
raw_D_shape_frame.grid(row=1, column=5, padx=5, pady=5,sticky="WENS")

# raw D shape orientation image frontend
image_tk8 = load_image("muvro/images/spring.jpg",150,150)
raw_d_img_lbl = Label(raw_D_shape_frame, image=image_tk8)
raw_d_img_lbl.image = image_tk8
raw_d_img_lbl.pack()


# ------------------------------------------------  section 2 starts here ------------------------------------------------------------------

main_frame = LabelFrame(root, text="Detection Results", font=("times new roman", 20, "bold"),
                        fg="black", bd=8, relief=GROOVE, bg=bg_color, padx=5, pady=5)
# main_frame.pack(fill=X)
main_frame.pack(fill=BOTH,expand=True)

main_frame.columnconfigure(0,weight=1)
main_frame.columnconfigure(1,weight=1)
main_frame.columnconfigure(2,weight=1)
main_frame.columnconfigure(3,weight=1)
main_frame.columnconfigure(4,weight=1)
main_frame.columnconfigure(5,weight=1)
main_frame.columnconfigure(6,weight=1)
main_frame.columnconfigure(7,weight=1)
main_frame.columnconfigure(8,weight=1)
main_frame.columnconfigure(9,weight=1)
main_frame.columnconfigure(10,weight=1)

main_frame.rowconfigure(0,weight=1)
main_frame.rowconfigure(1,weight=1)
main_frame.rowconfigure(2,weight=1)
main_frame.rowconfigure(3,weight=1)
main_frame.rowconfigure(4,weight=1)
main_frame.rowconfigure(5,weight=1)
main_frame.rowconfigure(6,weight=1)
main_frame.rowconfigure(7,weight=1)
main_frame.rowconfigure(8,weight=1)
main_frame.rowconfigure(9,weight=1)
main_frame.rowconfigure(10,weight=1)

# cam plate  Label frame
cam_plate_frame = LabelFrame(main_frame, text="Cam Plate", font=("times new roman", 15, "bold"), padx=10, pady=10)
cam_plate_frame.grid(row=0, column=0, padx=5, pady=5)

# moving plate image frontend
image_tk1 = load_image("muvro/images/cam_plate.jpg",130,130)
cam_img_lbl = Label(cam_plate_frame, image=image_tk1)
cam_img_lbl.image = image_tk1  # Store a reference to the image to prevent garbage collection
cam_img_lbl.pack()

# arrow code
canvas = Canvas(main_frame, width=40, height=25, bg=bg_color)
canvas.grid(row=0, column=1, padx=1, pady=30)
draw_forward_arrow(canvas)

# moving plate label frame
moving_plate_frame = LabelFrame(main_frame, text="Pin Returning Plate",font=("times new roman", 15, "bold"), padx=10, pady=10)
moving_plate_frame.grid(row=0, column=2, padx=5, pady=5)

# moving plate image frontend
image_tk1 = load_image("muvro/images/cam_plate.jpg",130,130)
moving_img_lbl = Label(moving_plate_frame, image=image_tk1)
moving_img_lbl.image = image_tk1  # Store a reference to the image to prevent garbage collection
moving_img_lbl.pack()

# arrow code
canvas = Canvas(main_frame, width=40, height=25, bg=bg_color)
canvas.grid(row=0, column=3, padx=1, pady=30)
draw_forward_arrow(canvas)


# spherical washer label frame
isolated_washer_frame = LabelFrame(main_frame, font=("times new roman", 15, "bold"), text="Isolated Plate", padx=10, pady=10)
isolated_washer_frame.grid(row=0, column=4, padx=5, pady=5)

# spherical washer image frontend
image_tk6 = load_image("muvro/images/spherical_washer.jpg",130,130)
isolated_img_lbl = Label(isolated_washer_frame, image=image_tk6)
isolated_img_lbl.image = image_tk6  # Store a reference to the image to prevent garbage collection
isolated_img_lbl.pack()

# arrow code
canvas = Canvas(main_frame, width=40, height=25, bg=bg_color)
canvas.grid(row=0, column=5, padx=1, pady=30)
draw_forward_arrow(canvas)
 

# spherical washer label frame
spherical_washer_frame = LabelFrame(main_frame, font=("times new roman", 15, "bold"), text="Flat Washer", padx=10, pady=10)
spherical_washer_frame.grid(row=0, column=6, padx=5, pady=5)

# spherical washer image frontend
image_tk6 = load_image("muvro/images/spherical_washer.jpg",130,130)
sph_img_lbl = Label(spherical_washer_frame, image=image_tk6)
sph_img_lbl.image = image_tk6  # Store a reference to the image to prevent garbage collection
sph_img_lbl.pack()

# arrow code
canvas = Canvas(main_frame, width=40, height=25, bg=bg_color)
canvas.grid(row=0, column=7, padx=1, pady=30)
draw_forward_arrow(canvas)

# bolts label frame
bolts_frame = LabelFrame(main_frame,font=("times new roman", 15, "bold"), text="Bolts", padx=10, pady=10)
bolts_frame.grid(row=0, column=8, padx=5, pady=5)

# bolts image frontend
image_tk7 = load_image("muvro/images/bolts.jpeg",130,130)
bolt_img_lbl = Label(bolts_frame, image=image_tk7)
bolt_img_lbl.image = image_tk7
bolt_img_lbl.pack()


# arrow code
canvas = Canvas(main_frame, width=40, height=25, bg=bg_color)
canvas.grid(row=0, column=9, padx=1, pady=30)
draw_forward_arrow(canvas)

# D shape orientation label frame
D_shape_frame = LabelFrame(main_frame, text="Pin",font=("times new roman", 15, "bold"), padx=10, pady=10)
D_shape_frame.grid(row=0, column=10, padx=5, pady=5)

# D shape orientation image frontend
image_tk8 = load_image("muvro/images/bolts.jpeg",130,130)
d_img_lbl = Label(D_shape_frame, image=image_tk8)
d_img_lbl.image = image_tk8
d_img_lbl.pack()


#     ------------------------------------       (Section 3)   After Assembly Details     --------------------------------------------------------------------------

#  details folder
details = LabelFrame(root, text="After Assembly Details", font=("times new roman", 20, "bold"),
                     fg="black", bd=8, relief=GROOVE, bg=bg_color)
# details.pack(fill=X)
details.pack(fill=BOTH,expand=True)


details.columnconfigure(0,weight=1)
details.columnconfigure(1,weight=1)
details.columnconfigure(2,weight=1)
details.columnconfigure(3,weight=1)

details.rowconfigure(0,weight=1)
details.rowconfigure(1,weight=1)
details.rowconfigure(2,weight=1)
details.rowconfigure(3,weight=1)

# ---------- Cam plate -------
y_cam_plate = Label(details, text=f"No. of detected Cam Plate : {cam_plate_yes}",
                     font=("times new roman", 12, "bold"), bg=bg_color)
y_cam_plate.grid(row=0, column=0, padx=10, pady=5,sticky="WENS")

no_cam_plate = Label(details, text=f"No. of not detected Cam Plate : {cam_plate_no}",
                      font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
no_cam_plate.grid(row=1, column=0, padx=10, pady=5,sticky="WENS")


# -------- moving plate --------
y_moving_plate = Label(details, text=f"No. of detected Pin Returning Plate : {moving_plate_yes}",
                        font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
y_moving_plate.grid(row=2, column=0, padx=10, pady=5,sticky="WENS")

no_moving_plate = Label(details, text=f"No. of not detected Pin Returning Plate : {moving_plate_no}",
                           font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
no_moving_plate.grid(row=3, column=0, padx=10, pady=5,sticky="WENS")


#  -------- spherical washer ------

y_spherical_washer = Label(details, text=f"No. of detected spherical Washer : {spherical_yes}",
                          font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
y_spherical_washer.grid(row=2, column=1, padx=10, pady=5,sticky="WENS")

no_spherical_washer = Label(details, text=f"No. of not detected spherical Washer : {spherical_no}",
                       font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
no_spherical_washer.grid(row=3, column=1, padx=10, pady=5,sticky="WENS")


# -------- bolts ----------
y_bolts = Label(details, text=f"No. of not detected Bolts : {bolt_no}",
                           font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
y_bolts.grid(row=0, column=2, padx=10, pady=5,sticky="WENS")

no_bolts = Label(details, text=f"No. of detected not Bolts : {bolt_yes}",
                          font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
no_bolts.grid(row=1, column=2, padx=10, pady=5,sticky="WENS")


# ----- D Shape Orientation --------
y_D_shape = Label(details, text=f"No. of detected pins : {shape_y}",
                       font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
y_D_shape.grid(row=2, column=2, padx=10, pady=5,sticky="WENS")

no_D_shape = Label(details, text=f"No. of detected not pins : {shape_n}",
                  font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
no_D_shape.grid(row=3, column=2, padx=10, pady=5,sticky="WENS")

# -------- isolated plate --------
y_isolated_plate = Label(details, text=f"No. of detected isolated Plate : {isolated_yes}",
                        font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
y_isolated_plate.grid(row=0, column=1, padx=10, pady=5,sticky="WENS")

no_isolated_plate = Label(details, text=f"No. of not detected isolated Plate : {isolated_no}",
                           font=("times new roman", 12, "bold"), bg=bg_color, bd=7)
no_isolated_plate.grid(row=1, column=1, padx=10, pady=5,sticky="WENS")


no_b = Label(details, text=f"Counter : {counter}",
                          font=("times new roman", 15, "bold"), bg=bg_color, bd=7)
no_b.grid(row=0, column=3, padx=10, pady=5,sticky="WENS")

work = Label(details,text="",font=("times new roman", 15, "bold") ,bg=bg_color)
work.grid(row=2, column=3, padx=10, pady=5,sticky="WENS")


# ================================================================================================================================================================
# ================================================================================================================================================================

if __name__ == "__main__":
    image_processing_thread_for_moving_plate = threading.Thread(target=check_components)
    image_processing_thread_for_moving_plate.start()
    print("ee")

    root.mainloop()
