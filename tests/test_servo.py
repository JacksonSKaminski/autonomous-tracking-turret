import board
import busio
import time
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

pan_servo = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
tilt_servo = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500)

for angle in range(0, 180, 10):
    print(f"Angle: {angle}")
    pan_servo.angle = angle
    tilt_servo.angle = angle
    time.sleep(0.5)

for angle in range(180, 0, -10):
    print(f"Angle: {angle}")
    pan_servo.angle = angle
    tilt_servo.angle = angle
    time.sleep(0.5)

pca.deinit()