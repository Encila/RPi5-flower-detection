# main_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
from model_predictor import ModelPredictor
import logging

class AppScreen(Screen):
    def __init__(self, model_path, labels_path, **kwargs):
        super().__init__(**kwargs)
        self.model_path = model_path
        self.labels_path = labels_path
        self.predictor = ModelPredictor(model_path, labels_path)
        self.capture = cv2.VideoCapture(0)

        self.layout = BoxLayout(orientation='vertical')
        self.image = Image()
        self.layout.add_widget(self.image)
        
        self.label = Label(size_hint=(1, 0.1))
        self.layout.add_widget(self.label)
        
        self.close_button = Button(text='Exit', size_hint=(1, 0.1))
        self.close_button.bind(on_press=self.close_application)
        self.layout.add_widget(self.close_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update_image, 1.0/30.0)

    def update_image(self, dt):
        logging.debug("Updating image...")
        ret, frame = self.capture.read()
        if ret:
            class_id, confidence = self.predictor.predict(frame)
            label = f"{self.predictor.labels[class_id]} ({confidence * 100:.2f}%)"
            self.label.text = label

            threshold = 0.5
            if confidence > threshold:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    c = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    label_x = x if x + w + 10 < self.image.width else x - w
                    label_y = y - 10 if y - 10 > 0 else y + h + 20

                    cv2.putText(frame, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def close_application(self, instance):
        logging.info("Closing application...")
        App.get_running_app().stop()
        self.capture.release()
