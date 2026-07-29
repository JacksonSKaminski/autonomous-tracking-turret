class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def update(self, error):
        self.integral += error

        P_term = self.kp * error
        D_term = self.kd * (error - self.prev_error)
        I_term = self.ki * self.integral

        self.prev_error = error

        return P_term + I_term + D_term

    def reset(self):
        self.prev_error = 0
        self.integral = 0