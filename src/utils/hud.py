import cv2 as cv

def draw_hud(frame, roe_state, tracker_state, angle_x, angle_y, pan_output, tilt_output, latency_ms):
    """
    Draws the HUD (Heads-Up Display) on the given frame.

    Args:
        frame (numpy.ndarray): The frame on which to draw the HUD.
        roe_state (str): The current state of the ROE (Rules of Engagement).
        tracker_state (dict): The current state of the tracker.
        angle_x (float): The pan angle error in degrees.
        angle_y (float): The tilt angle error in degrees.
        pan_output (float): The output from the pan PID controller.
        tilt_output (float): The output from the tilt PID controller.
        latency_ms (float): The latency in milliseconds.
    """

    #Top Left
    cv.putText(frame, f"ROE State: {roe_state}", (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Tracker Age: {tracker_state['track_age']}", (10, 55), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Frames Since Detection: {tracker_state['frames_since_detection']}", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Latency: {latency_ms:.2f} ms", (10, 100), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    #Bottom Left
    cv.putText(frame, f"Pan Error: {angle_x:.2f}°", (10, frame.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Tilt Error: {angle_y:.2f}°", (10, frame.shape[0] - 55), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Pan PID Output: {pan_output:.2f}", (10, frame.shape[0] - 90), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Tilt PID Output: {tilt_output:.2f}", (10, frame.shape[0] - 125), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)  

    #Top Right
    cv.putText(frame, f"Tracker Position: ({tracker_state['cx']:.2f}, {tracker_state['cy']:.2f})", (frame.shape[1] - 400, 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv.putText(frame, f"Tracker Velocity: ({tracker_state['vx']:.2f}, {tracker_state['vy']:.2f})", (frame.shape[1] - 400, 55), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)