import numpy as np
import imutils
import easyocr
import cv2
import color
import os
import os.path
from datetime import date
import time
from db import dataBase

class Camera_det(object):
    def __init__(self):
        self.camera_type = "entry"
        self.camera_loc = "Gate-01"
        self.parkingStat = "no"

def feature_veh(img):
    col = color.ret_color(img)
    return col

def number_plate(img):
    img = cv2.resize(img, (620,480) )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    path = './'
    cv2.imwrite(os.path.join(path , 'check.jpg'), img)

    bfilter=cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection

    #contour detection - shapes basically
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#approximate the contour
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #top 10 contours

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)#allows to approximate the polygon from our contour, rough sides
        if len(approx) == 4:   #if the approximation has 4 keypoints -- number plate location
            location = approx
            break
    location

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y)) #top left corner
    (x2, y2) = (np.max(x), np.max(y))  #bottom right corner
    cropped_image = gray[x1:x2+1, y1:y2+1] #buffer +1


    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    # print(result)
    text = result[0][1] #+ result[1][1]
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    #res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
    return text

if __name__ == "__main__":
    dBase = dataBase()
    num = 0
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    today = date.today()
    #print(current_time)
    #print("Today's date:", today)
    obj = Camera_det()
    #print(obj.camera_type)
    #print(obj.camera_loc)
    #parkingStat = "no" parking status

    cap = cv2.VideoCapture(0)
    (ret, frame) = cap.read()

    while (cap.isOpened()):
        ret, img = cap.read()
         
        if ret == True:
            cv2.imshow('original video', img)
             
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            plate = number_plate(img)
            print(plate) # plate no.

            if plate is not None:
                color = feature_veh(img)
                print(color) # vehicle color
                break
            
            num += 1
            dBase.insertDataBase(num, plate, color, obj.camera_type, current_time, parkingStat)


    cap.release()
    cv2.destroyAllWindows()	
            