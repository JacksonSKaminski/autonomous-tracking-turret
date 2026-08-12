import time
import cv2 as cv

from src.utils.camera import Camera
from src.detection.detector import Detector
from src.tracking.tracker import Tracker
from src.control.roe import ROE
from src.control.pid import PID

from src.utils.coordinate import pixel_error_to_angle
from src.utils.hud import draw_hud

camera = Camera() #Initialize the camera
detector = Detector("yolov8n.pt")  # Load the YOLOv8 model
tracker = Tracker()  # Initialize the tracker
roe = ROE()  # Initialize the ROE

pan_pid = PID(kp=0.1, ki=0.0, kd=0.05)  # Initialize PID controller for pan
tilt_pid = PID(kp=0.1, ki=0.0, kd=0.05)  # Initialize PID controller for tilt

frame_width, frame_height = camera.get_resolution()

prev_roe_state = "SEARCH"

run = True
while run:
    loop_start_time = time.time()  # Start time for latency calculation

    #Gets frame from camera
    frame = camera.get_frame()
    if frame is None:
        continue

    #Run Interference and return detections
    detections = detector.detect(frame)

    tracker.predict()

    if detections:
        best = max(detections, key=lambda x: x["confidence"])  # Get the detection with the highest confidence
        tracker.update(best["centroid"][0], best["centroid"][1])  # Update Tracker with new detection

        cv.rectangle(frame, (int(best["bounding_box"][0]), int(best["bounding_box"][1])), (int(best["bounding_box"][2]), int(best["bounding_box"][3])), (0, 255, 0), 2)
        cv.circle(frame, (int(best["centroid"][0]), int(best["centroid"][1])), 5, (0, 0, 255), -1)
        cv.putText(frame, f"Class: {best['class_name']}, Confidence: {best['confidence']:.2f}", (int(best["bounding_box"][0]), int(best["bounding_box"][1]) - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    tracker_state = tracker.get_state()
    print(f"Tracker State: {tracker_state}")

    roe_state = roe.update_state(detections, tracker_state)
    print(f"ROE State: {roe_state}")

    if roe_state == "SEARCH" and prev_roe_state == "HOLD":
        tracker.reset()

    error_x = tracker_state["cx"] - frame_width / 2
    error_y = tracker_state["cy"] - frame_height / 2

    angle_x, angle_y = pixel_error_to_angle(error_x, error_y, frame_width, frame_height)
    print(f"Pan error: {angle_x:.2f}°, Tilt error: {angle_y:.2f}°")

    if roe_state == "SEARCH":
        pan_pid.reset()
        tilt_pid.reset()
    elif roe_state == "TRACK":
        pan_output = pan_pid.update(angle_x)
        tilt_output = tilt_pid.update(angle_y)

        print(f"Pan PID output: {pan_output:.2f}, Tilt PID output: {tilt_output:.2f}")

    prev_roe_state = roe_state
    latency = (time.time() - loop_start_time) * 1000  # Calculate latency in milliseconds

    draw_hud(frame, roe_state, tracker_state, angle_x, angle_y, pan_output if roe_state == "TRACK" else 0, tilt_output if roe_state == "TRACK" else 0, latency)

    cv.imshow('Camera Feed', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        run = False

camera.release()