# waiting_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse

class RoundButton(Button):
    def __init__(self, **kwargs):
        super(RoundButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.ellipse = Ellipse(size=self.size, pos=self.pos)
            self.bind(pos=self.update_ellipse, size=self.update_ellipse)

    def update_ellipse(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size

class WaitingScreen(Screen):
    def __init__(self, model_path, labels_path, **kwargs):
        super().__init__(**kwargs)
        self.model_path = model_path
        self.labels_path = labels_path

        layout = FloatLayout()

        self.label = Label(
            text="Press the button to start flower recognition",
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )

        self.start_button = RoundButton(
            text="",
            size_hint=(0.2, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            background_normal='',
            background_color=(1, 1, 1, 1)
        )
        camera_icon = Image(source='camera_icon.png', size_hint=(0.5, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.start_button.add_widget(camera_icon)
        self.start_button.bind(on_press=self.start_recognition)

        self.close_button = Button(
            text="X",
            size_hint=(0.1, 0.1),
            pos_hint={"right": 1, "top": 1}
        )
        self.close_button.bind(on_press=self.close_application)

        layout.add_widget(self.label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.close_button)

        self.add_widget(layout)

    def start_recognition(self, instance):
        self.manager.current = 'main_screen'

    def close_application(self, instance):
        App.get_running_app().stop()
        Window.close()
