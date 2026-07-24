import numpy as np

class Tracker:
    def __init__(self):
        '''
        Initializes the Tracker with a Kalman filter for tracking object positions.
        '''
        
        self.x = np.zeros((4, 1)) #State vector [x, y, dx, dy]
        self.P = np.eye(4) #Covariance matrix
        self.Q = np.diag([0.1, 0.1, 0.01, 0.01]) #Process noise covariance
        self.R = np.diag([2.0, 2.0]) #Measurement noise covariance
        self.F = np.array([[1, 0, 1, 0],
                           [0, 1, 0, 1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=float) #State transition matrix
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]], dtype=float) #Measurement matrix

        self.x_predicted = np.zeros((4, 1)) #Predicted state vector
        self.P_predicted = np.eye(4) #Predicted covariance matrix

        self.initialized = False
        self.track_age = 0
        self.frames_since_detection = 0

    def predict(self):
        '''
        Predicts the next state of the tracker using the Kalman filter equations.
        '''

        self.x_predicted = self.F @ self.x #Predicted state estimate
        self.P_predicted = self.F @ self.P @ self.F.T + self.Q #Predicted covariance estimate

        self.x = self.x_predicted
        self.P = self.P_predicted

        self.track_age = 0
        self.frames_since_detection += 1

    def update(self, cx, cy):
        '''
        Updates the tracker with a new measurement (centroid) using the Kalman filter equations.
        '''

        if not self.initialized: #Initialize the state vector with the first detection
            self.x[0] = cx
            self.x[1] = cy
            self.initialized = True
            return

        z = np.array([[cx], [cy]]) #Measurement vector
        y = z - self.H @ self.x_predicted #Innovation
        S = self.H @ self.P_predicted @ self.H.T + self.R #Innovation covariance
        K = self.P_predicted @ self.H.T @ np.linalg.inv(S) #Kalman gain

        self.x = self.x_predicted + K @ y #Update state estimate
        self.P = (np.eye(4) - K @ self.H) @ self.P_predicted #Update covariance estimate

        self.track_age += 1
        self.frames_since_detection = 0

    def get_state(self):
        '''
        Returns the current state of the tracker, including position, velocity, and track age.

        Returns:
            dict: A dictionary containing the current state of the tracker with keys "cx", "cy", "vx", "vy", and "track_age".
        '''

        return {
            "cx": float(self.x[0,0]),
            "cy": float(self.x[1,0]),
            "vx": float(self.x[2,0]),
            "vy": float(self.x[3,0]),
            "track_age": self.track_age,
            "frames_since_detection": self.frames_since_detection
        }


if __name__ == "__main__":
    detections = [
        {"frame": 1,  "cx": 302, "cy": 241},
        {"frame": 2,  "cx": 308, "cy": 243},
        {"frame": 3,  "cx": 315, "cy": 246},
        {"frame": 4,  "cx": 321, "cy": 248},
        {"frame": 5,  "cx": 329, "cy": 251},
        {"frame": 6,  "cx": None, "cy": None},  # occluded
        {"frame": 7,  "cx": None, "cy": None},  # occluded
        {"frame": 8,  "cx": 342, "cy": 257},
        {"frame": 9,  "cx": 349, "cy": 259},
        {"frame": 10, "cx": 356, "cy": 262},
    ]

    tracker = Tracker()

    for detection in detections:
        tracker.predict()

        if detection["cx"] is not None and detection["cy"] is not None:
            tracker.update(detection["cx"], detection["cy"])

        print(f"Frame {detection['frame']}: Predicted Position: ({tracker.x[0, 0]:.2f}, {tracker.x[1, 0]:.2f}).  Actual Position: ({detection['cx']}, {detection['cy']}).  Covariance: {tracker.P[0, 0]:.2f}, {tracker.P[1, 1]:.2f}.  State: {tracker.x.flatten()}")