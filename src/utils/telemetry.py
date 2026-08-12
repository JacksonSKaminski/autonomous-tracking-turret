import csv
import time

class TelemetryLogger:
    def __init__(self, log_file_path="logs/"):
        file_name = f"telemetry_log_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = log_file_path + file_name

        self.log_file = open(file_path, mode='w', newline='')
        self.csv_writer = csv.writer(self.log_file)
        self.csv_writer.writerow(["Timestamp", "ROE State", "cx", "cy", "vx", "vy", "track_age", "Angle X", "Angle Y", "Pan Output", "Tilt Output", "Latency (ms)"])

    def log(self, roe_state, tracker_state, angle_x, angle_y, pan_output, tilt_output, latency_ms):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.csv_writer.writerow([
            timestamp,
            roe_state,
            tracker_state['cx'],
            tracker_state['cy'],
            tracker_state['vx'],
            tracker_state['vy'],
            tracker_state['track_age'],
            angle_x,
            angle_y,
            pan_output,
            tilt_output,
            latency_ms
        ])

    def close(self):
        self.log_file.close()