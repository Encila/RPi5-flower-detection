from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time
from picamera2 import Picamera2
import logging

class VideoThreadPiCam(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, process_every_n_frames=5):
        super().__init__()
        self.grab_frame = True
        self.process_every_n_frames = process_every_n_frames
        self.frame_count = 0

    def run(self):
        try:
            logging.info("Initializing camera...")
            picam2 = Picamera2()
            camera_config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, raw={"size": (640, 480)})
            picam2.configure(camera_config)
            picam2.start()
            logging.info("Camera started.")

            while True:
                if self.grab_frame:
                    frame = picam2.capture_array()
                    self.frame_count += 1
                    if self.frame_count % self.process_every_n_frames == 0:
                        logging.debug("Emitting frame...")
                        self.change_pixmap_signal.emit(frame)
                    self.grab_frame = False
                else:
                    time.sleep(0.0001)
        except Exception as e:
            logging.error(f"Error in video thread: {e}")
