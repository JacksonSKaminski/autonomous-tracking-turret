import cv2 as cv
import numpy as np
import time

USE_PI_CAMERA = False

class Camera:
    """
    Camera class for capturing frames from a camera.
    This class supports both Pi camera and standard USB cameras.
    """
    def __init__(self):
        self.prevTime = None
        self.fps = 0.0

        if (USE_PI_CAMERA):
            raise NotImplementedError("Pi camera not implemented yet")
        
        else:
            self.cap = cv.VideoCapture(0)

    def get_frame(self):
        """
        Gets a frame from the camera
        
        Returns:
            frame (numpy.ndarray): The captured frame from the camera.
        """

        now = time.time()

        #Fps Calculation
        if self.prevTime is not None:
            self.fps = 1.0 / (now - self.prevTime)
        self.prevTime = now
        
        if (USE_PI_CAMERA):
            raise NotImplementedError("Pi camera not implemented yet")
        
        else:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to capture frame from camera.")
                return None

            return frame      

    def release(self):
        """
        Releases the camera resources and closes any OpenCV windows.
        """
        self.cap.release()  
        cv.destroyAllWindows()


if __name__ == "__main__":
    camera = Camera()
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

        #Frame Counter for Displaying FPS
        frameCount += 1
        if frameCount % 30 == 0:
            print(f"FPS: {camera.fps:.1f}")


    camera.release()