# display.py
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

        # Camera display area
        self.image = Image()
        self.layout.add_widget(self.image)

        # Control buttons layout
        controls_layout = BoxLayout(size_hint=(1, 0.2), padding=20, spacing=10)

        # Create the circular camera button
        self.camera_button = Button(
            size_hint=(None, None),
            size=(80, 80),
            background_normal='',
            background_color=(1, 1, 1, 1),  # White background
            border=(0, 0, 0, 0)
        )
        self.camera_button.bind(on_press=self.take_picture)

        # Add a circular border to the camera button
        with self.camera_button.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.circle = Ellipse(size=(80, 80), pos=self.camera_button.pos)

        self.camera_button.bind(pos=self.update_circle, size=self.update_circle)

        controls_layout.add_widget(self.camera_button)
        self.layout.add_widget(controls_layout)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update_image, 1.0 / 30.0)

    def update_circle(self, *args):
        self.circle.pos = self.camera_button.pos
        self.circle.size = self.camera_button.size

    def update_image(self, dt):
        logging.debug("Updating image...")
        ret, frame = self.capture.read()
        if ret:
            class_id, confidence = self.predictor.predict(frame)
            label = f"{self.predictor.labels[class_id]} ({confidence * 100:.2f}%)"
            self.label.text = label

            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def take_picture(self, instance):
        # Logic to take a picture
        logging.info("Picture taken!")

    def close_application(self, instance):
        logging.info("Closing application...")
        App.get_running_app().stop()
        self.capture.release