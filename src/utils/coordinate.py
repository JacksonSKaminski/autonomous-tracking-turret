def pixel_error_to_angle(error_x, error_y, frame_width, frame_height, fov_horizontal=60, fov_vertical=40):
    degrees_per_pixel_x = fov_horizontal / frame_width
    degrees_per_pixel_y = fov_vertical / frame_height
    
    angle_x = error_x * degrees_per_pixel_x
    angle_y = error_y * degrees_per_pixel_y
    
    return angle_x, angle_y