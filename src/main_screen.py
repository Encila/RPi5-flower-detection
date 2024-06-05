# main_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

class MainScreen(Screen):
    def __init__(self, model_path, labels_path, **kwargs):
        super().__init__(**kwargs)
        self.model_path = model_path
        self.labels_path = labels_path

        layout = FloatLayout()

        self.label = Label(
            text="Flower Recognition in progress...",
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )

        self.image = Image(
            size_hint=(1, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.3}
        )

        self.close_button = Button(
            text="Exit",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.1}
        )
        self.close_button.bind(on_press=self.close_application)

        layout.add_widget(self.label)
        layout.add_widget(self.image)
        layout.add_widget(self.close_button)

        self.add_widget(layout)

    def update_image(self, image):
        self.image.texture = image

    def close_application(self, instance):
        App.get_running_app().stop()
        Window.close()
