from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window

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

        self.start_button = Button(
            text="Start Recognition",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.4}
        )
        self.start_button.bind(on_press=self.start_recognition)

        self.close_button = Button(
            text="Exit",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.2}
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