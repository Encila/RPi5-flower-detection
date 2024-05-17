from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt
import cv2
import numpy as np
import logging
from model_predictor import ModelPredictor

class App(QWidget):
    """
    A class to represent the application GUI.

    Attributes:
    camera_test_only (bool): Flag to determine if only the camera test is running.
    model_path (str): Path to the model file.
    """
    def __init__(self, camera_test_only, model_path, labels_path):
        super().__init__()
        self.camera_test_only = camera_test_only
        self.setWindowTitle("Qt UI")
        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)
        self.predictor = ModelPredictor(model_path, labels_path)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        logging.debug("Updating image...")
        class_id, confidence = self.predictor.predict(cv_img)
        label = f"{self.predictor.labels[class_id]} ({confidence * 100:.2f}%)"
        
        threshold = 0.5
        if confidence > threshold:
            gray = cv2.cvt
