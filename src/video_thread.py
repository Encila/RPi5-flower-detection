from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time
from picamera2 import Picamera2

class VideoThreadPiCam(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.grab_frame = True

    def run(self):
        picam2 = Picamera2()
        camera_config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, raw={"size": (640, 480)})
        picam2.configure(camera_config)
        picam2.start()

        while True:
            if self.grab_frame:
                frame = picam2.capture_array()
                self.change_pixmap_signal.emit(frame)
                self.grab_frame = False
            else:
                time.sleep(0.0001)
