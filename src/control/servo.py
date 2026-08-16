from adafruit_motor import servo

class ServoController:
    def __init__(self, pca, channel, min_pulse=500, max_pulse=2500, min_angle = 10, max_angle = 170):
        self.servo = servo.Servo(pca.channels[channel], min_pulse=min_pulse, max_pulse=max_pulse)
        self.angle = 90
        self.min_angle = min_angle
        self.max_angle = max_angle
    
    def update(self, delta):
        new_angle = self.angle + delta
        new_angle = max(self.min_angle, min(self.max_angle, new_angle))  # Clamp the angle between min_angle and max_angle
        self.servo.angle = new_angle
        self.angle = new_angle