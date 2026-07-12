import cv2 as cv
import numpy as np
import time

USE_PI_CAMERA = False

#Camera Class
class Camera:
    #Initialize Camera 
    def __init__(self):
        if (USE_PI_CAMERA):
            raise NotImplementedError("Pi camera not implemented yet")
        
        else:
            self.cap = cv.VideoCapture(0)

    #Get a frame
    def get_frame(self):
        if (USE_PI_CAMERA):
            raise NotImplementedError("Pi camera not implemented yet")
        
        else:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to capture frame from camera.")
                return None

            return frame      

    #Release Camera
    def release(self):
        self.cap.release()  
        cv.destroyAllWindows()

camera = Camera()
previousTime = time.time()
frameCount = 0

#Main Loop
run = True
while run:
    #Displays Feed
    frame = camera.get_frame()
    if frame is not None:
        cv.imshow('Camera Feed', frame)

    #Exit Feed
    if cv.waitKey(1) & 0xFF == ord('q'):
        run = False

    #FPS Calculation
    currentTime = time.time()
    fps = 1.0 / (currentTime - previousTime)
    previousTime = currentTime

    #Frame Counter for Displaying FPS
    frameCount += 1
    if frameCount % 30 == 0:
        print(f"FPS: {fps:.1f}")


camera.release()