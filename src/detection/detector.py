from ultralytics import YOLO

TARGET_CLASSES = {0: "person", 2: "car", 7: "truck"}
CONFIDENCE_THRESHOLD = 0.5

class Detector:
    """
    Detector class for object detection using YOLOv8.
    This class loads a YOLOv8 model and provides a method to detect objects in frames"""
   
    def __init__(self, model_path):
        '''
        Initializes the Detector with a YOLOv8 model.
        '''
        self.model = YOLO(model_path)

    def detect(self, frame):
        '''
        Run interference on a single frame and return the filtered detections.
        
        Args:
            frame: The input frame for object detection. Numpy array of shape (height, width, 3)
        
        Returns:
            List of dicts with keys: class_id, class_name, confidence, bbox, centroid
        '''

        results = self.model(frame)

        detections = []
    
        for box in results[0].boxes:

            #Filter by Confidence Threshold and Target Classes
            if box.conf[0].item() < CONFIDENCE_THRESHOLD:
                continue
            if box.cls[0].item() not in TARGET_CLASSES:
                continue

            # Access the bounding box coordinates and class label
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Bounding box coordinates
            cx = int((x1 + x2) / 2)  # Center x-coordinate
            cy = int((y1 + y2) / 2)  # Center y-coordinate
            
            class_id = int(box.cls[0].item())  # Class label index
            confidence = float(box.conf[0].item())  # Confidence score
            
            detections.append({
                "class_id": class_id,
                "class_name": TARGET_CLASSES[class_id],
                "confidence": confidence,
                "bounding_box": (x1, y1, x2, y2),
                "centroid": (cx, cy)
            })

        return detections