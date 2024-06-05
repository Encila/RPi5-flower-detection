import sys
import argparse
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from waiting_screen import WaitingScreen

def setup_logging():
    import logging
    import coloredlogs

    custom_colors = {
        'debug': {'color': 'green'},
        'info': {'color': 'white'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red', 'bold': True},
        'critical': {'color': 'magenta', 'bold': True},
    }

    field_styles = {
        'asctime': {'color': 'white'},
        'levelname': {'color': 'green', 'bold': True},
        'message': {'color': 'white'}
    }

    logger = logging.getLogger(__name__)
    coloredlogs.install(level='INFO', logger=logger, fmt='[%(asctime)s] [%(process)d] %(levelname)s %(message)s', level_styles=custom_colors, field_styles=field_styles)

class FlowerRecognitionApp():
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", default="models/v1/model.tflite")
        parser.add_argument("--labels", default="models/v1/labels.txt")

        args = parser.parse_args()

        sm = ScreenManager()
        sm.add_widget(WaitingScreen(name='waiting_screen'), model_path=args.model, labels_path=args.labels)
        return sm

if __name__ == "__main__":
    setup_logging()
    FlowerRecognitionApp().run()
