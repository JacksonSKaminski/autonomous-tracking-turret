# System Architecture

## Overview

This system is an autonomous multi-class target tracking turret built on a Raspberry Pi. A camera feeds frames into a computer vision pipeline that detects and classifies objects

---

## Data Flow

```
Camera Frame (numpy array: height x width x 3)
        ↓
    Detector
    YOLOv8n inference → list of detections [{class_id, class_name, confidence, bbox, centroid}]
        ↓
    Kalman Filter Tracker
    Predict + update cycle → smoothed centroid, velocity estimate
```

---

## Component Breakdown

### 1. Camera (`src/utils/camera.py`)

A hardware abstraction layer around the camera input. Wraps both `cv2.VideoCapture` (Mac/USB webcam) and `picamera2` (Raspberry Pi CSI ribbon cable camera) behind a consistent interface. The rest of the pipeline calls `get_frame()` and receives a numpy array — it never interacts with the camera hardware directly.

**Input:** none  
**Output:** numpy array of shape `(height, width, 3)`, dtype uint8

### 2. Detector (`src/detection/detector.py`)

Runs YOLOv8n inference on each frame. Filters detections by target class (person, car, truck) and confidence threshold (0.5). Computes the centroid of each bounding box for use by the tracker.

**Input:** numpy array (camera frame)  
**Output:** list of detection dictionaries containing class ID, class name, confidence score, bounding box coordinates, and centroid


---

## Folder Structure

```
autonomous-tracking-turret/
├── main.py
├── requirements.txt
├── src/
│   ├── detection/
│   │   └── detector.py
│   ├── tracking/
│   │   └── tracker.py
│   ├── control/
│   └── utils/
├── docs/
   └── architecture.md
```

---

## Performance targets

- Detection model: YOLOv8n (~6MB weights)
- Target platform: Raspberry Pi 4