import cv2
import base64
import datetime
from .log import Logger

now = datetime.datetime.now()

log = Logger()

class CameraScreenshotter:
    def __init__(self, camera_url):
        self.camera_url = camera_url
        self.video_capture = None
    
    def open_stream(self):
        self.video_capture = cv2.VideoCapture(self.camera_url)
        if not self.video_capture.isOpened():
            log.error("Failed to open camera stream")
    
    def capture_screenshot(self, output_path, max_width=640, max_height=480):
        if self.video_capture is None or not self.video_capture.isOpened():
            print("Camera stream is not opened")
            return
        
        ret, frame = self.video_capture.read()
        
        if not ret:
            log.error("Failed to read frame from camera stream")
            return
        
        # Get the original image dimensions
        original_height, original_width = frame.shape[:2]
        
        # Calculate the scaling factor to downsample the image while maintaining aspect ratio
        scale_factor = min(max_width / original_width, max_height / original_height)
        
        # Calculate the new dimensions based on the scaling factor
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Resize the image
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        cv2.imwrite(output_path, resized_frame)
        log.info("Screenshot saved to {}".format(output_path))
    
    def close_stream(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None
            log.info("Camera stream closed")

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")




            