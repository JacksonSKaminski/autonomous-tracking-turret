from src.utils.camera import Camera
from src.detection.detector import Detector
from src.tracking.tracker import Tracker
from src.control.roe import ROE as roe
import cv2 as cv

from utils.coordinate import pixel_error_to_angle

camera = Camera()
detector = Detector("yolov8n.pt")  # Load the YOLOv8 model
tracker = Tracker()  # Initialize the tracker

frame_width, frame_height = camera.get_resolution()

run = True
while run:
    frame = camera.get_frame()
    if frame is None:
        continue

    detections = detector.detect(frame)

    tracker.predict()

    state = roe.update_state(detections, tracker.get_state())
    print(state)

    if detections:
        best = max(detections, key=lambda x: x["confidence"])  # Get the detection with the highest confidence
        tracker.update(best["centroid"][0], best["centroid"][1])  

        cv.rectangle(frame, (int(best["bounding_box"][0]), int(best["bounding_box"][1])),                   (int(best["bounding_box"][2]), int(best["bounding_box"][3])), (0, 255, 0), 2)
        cv.circle(frame, (int(best["centroid"][0]), int(best["centroid"][1])), 5, (0, 0, 255), -1)
        cv.putText(frame, f"Class: {best['class_name']}, Confidence: {best['confidence']:.2f}", (int(best["bounding_box"][0]), int(best["bounding_box"][1]) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    state = roe.update_state(detections, tracker.get_state())

    error_x = state["cx"] - frame_width / 2
    error_y = state["cy"] - frame_height / 2
    angle_x, angle_y = pixel_error_to_angle(error_x, error_y, frame_width, frame_height)
    print(f"Pan error: {angle_x:.2f}°, Tilt error: {angle_y:.2f}°")

    cv.imshow('Camera Feed', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        run = False

camera.release()