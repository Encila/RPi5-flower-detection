from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt
import cv2
import numpy as np
from model_predictor import ModelPredictor
import logging
class App(QWidget):
    def __init__(self, model_path, labels_path):
        super().__init__()
        self.setWindowTitle("Flower Detection App")
        self.display_width = 2592
        self.display_height = 2592
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)
        self.predictor = ModelPredictor(model_path, labels_path)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        logging.info("Updating image...")
        class_id, confidence = self.predictor.predict(cv_img)
        label = f"{self.predictor.labels[class_id]} ({confidence * 100:.2f}%)"
        
        threshold = 0.5
        if confidence > threshold:
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                c = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                label_x = x if x + w + 10 < self.display_width else x - w
                label_y = y - 10 if y - 10 > 0 else y + h + 20

                cv2.putText(cv_img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        self.thread.grab_frame = True

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)
