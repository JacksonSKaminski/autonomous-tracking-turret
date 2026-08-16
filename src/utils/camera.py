import cv2 as cv
import numpy as np
import time

USE_PI_CAMERA = True

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
    print("Picamera2 library not found. Falling back to standard USB camera.")

class Camera:
    """
    Camera class for capturing frames from a camera.
    This class supports both Pi camera and standard USB cameras.
    """
    def __init__(self, USE_PI_CAMERA=False):
        self.prevTime = None
        self.fps = 0.0
        self.USE_PI_CAMERA = USE_PI_CAMERA and PICAMERA2_AVAILABLE

        if (self.USE_PI_CAMERA):
            self.picam2 = Picamera2()

            config = self.picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
            self.picam2.configure(config)

            self.picam2.start()

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
        
        if (self.USE_PI_CAMERA):
            frame = self.picam2.capture_array()

            frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR) # Convert RGB to BGR for OpenCV compatibility

            return frame
        
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

        if (self.USE_PI_CAMERA):
            self.picam2.stop()
        else:
            self.cap.release()  
            
        cv.destroyAllWindows()

    def get_resolution(self):
        """
        Gets the resolution of the camera
        
        Returns:
            (width, height) (tuple): The width and height of the camera resolution.
        """
        if (self.USE_PI_CAMERA):
            return (640, 480)
        
        else:
            width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            return (width, height)


if __name__ == "__main__":
    camera = Camera()

    #Main Loop
    run = True
    while run:
        #Displays Feed
        frame = camera.get_frame()
        if frame is not None:
            if USE_PI_CAMERA:    
                cv.imshow('Camera Feed', frame)
            print(f"Frame Shape: {frame.shape}, FPS: {camera.fps:.1f}")

        #Exit Feed
        if cv.waitKey(1) & 0xFF == ord('q'):
            run = False

    camera.release()