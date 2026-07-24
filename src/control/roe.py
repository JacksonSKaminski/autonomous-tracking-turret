class ROE:
    def __init__(self, confidence_threshold=0.7, max_frames_since_detection = 30, min_track_age=3):
        self.STATE = "SEARCH"
        self.CONFIDENCE_THRESHOLD = confidence_threshold
        self.MIN_TRACK_AGE = min_track_age
        self.MAX_FRAMES_SINCE_DETECTION = max_frames_since_detection

    def update_state(self, detections, tracker_state):
        if detections:
            best = max(detections, key=lambda d: d["confidence"])

        match self.STATE:
            case "SEARCH":
                if detections and best["confidence"] > self.CONFIDENCE_THRESHOLD and tracker_state["track_age"] > self.MIN_TRACK_AGE:
                    self.STATE = "TRACK"

                return self.STATE
            
            case "TRACK":
                if not detections or tracker_state["frames_since_detection"] > self.MAX_FRAMES_SINCE_DETECTION:
                    self.STATE = "HOLD"

                return self.STATE
            
            case "HOLD":
                if detections and best["confidence"] > self.CONFIDENCE_THRESHOLD and tracker_state["track_age"] > self.MIN_TRACK_AGE:
                    self.STATE = "TRACK"

                if not detections and tracker_state["frames_since_detection"] > self.MAX_FRAMES_SINCE_DETECTION:
                    self.STATE = "SEARCH"
                    
                return self.STATE
 
