from ultralytics import YOLO

class Detector:
    """
    Detector class for object detection using YOLOv8.
    This class loads a YOLOv8 model and provides a method to detect objects in frames"""
   
    def __init__(self, model_path, confidence_threshold = 0.5, target_classes = None):
        '''
        Initializes the Detector with a YOLOv8 model.
        '''
        self.model = YOLO(model_path)
        
        if target_classes is None:
            target_classes = {0: "person", 2: "car", 7: "truck"}
        self.target_classes = target_classes
        self.confidence_threshold = confidence_threshold

    def detect(self, frame):
        '''
        Run inference on a single frame and return the filtered detections.
        
        Args:
            frame: The input frame for object detection. Numpy array of shape (height, width, 3)
        
        Returns:
            List of dicts with keys: class_id, class_name, confidence, bbox, centroid
        '''

        results = self.model(frame)

        detections = []
    
        for box in results[0].boxes:

            #Filter by Confidence Threshold and Target Classes
            if box.conf[0].item() < self.confidence_threshold:
                continue
            if box.cls[0].item() not in self.target_classes:
                continue

            # Access the bounding box coordinates and class label
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Bounding box coordinates
            cx = int((x1 + x2) / 2)  # Center x-coordinate
            cy = int((y1 + y2) / 2)  # Center y-coordinate
            
            class_id = int(box.cls[0].item())  # Class label index
            confidence = float(box.conf[0].item())  # Confidence score
            
            detections.append({
                "class_id": class_id,
                "class_name": self.target_classes[class_id],
                "confidence": confidence,
                "bounding_box": (x1, y1, x2, y2),
                "centroid": (cx, cy)
            })

        return detections