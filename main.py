from src.utils.camera import Camera
from src.detection.detector import Detector
import cv2 as cv
import time

camera = Camera()
detector = Detector("yolov8n.pt")  # Load the YOLOv8 model

run = True
while run:
    frame = camera.get_frame()
    if frame is None:
        continue

    results = detector.detect(frame)
    print(results)

    run = False
    
