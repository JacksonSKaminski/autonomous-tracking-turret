from src.utils.camera import Camera
from src.detection.detector import Detector
from src.tracking.tracker import Tracker
import cv2 as cv

camera = Camera()
detector = Detector("yolov8n.pt")  # Load the YOLOv8 model
tracker = Tracker()  # Initialize the tracker

run = True
while run:
    frame = camera.get_frame()
    if frame is None:
        continue

    detections = detector.detect(frame)

    tracker.predict()
    if detections:
        best = max(detections, key=lambda x: x["confidence"])  # Get the detection with the highest confidence
        tracker.update(best["centroid"][0], best["centroid"][1])  

        cv.rectangle(frame, (int(best["bounding_box"][0]), int(best["bounding_box"][1])),                   (int(best["bounding_box"][2]), int(best["bounding_box"][3])), (0, 255, 0), 2)
        cv.circle(frame, (int(best["centroid"][0]), int(best["centroid"][1])), 5, (0, 0, 255), -1)
        cv.putText(frame, f"Class: {best['class_name']}, Confidence: {best['confidence']:.2f}", (int(best["bounding_box"][0]), int(best["bounding_box"][1]) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv.imshow('Camera Feed', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        run = False

camera.release()