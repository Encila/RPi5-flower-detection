import sys
import argparse
from PyQt5.QtWidgets import QApplication
from display import App
from video_thread import VideoThreadPiCam
import logging
import coloredlogs

def setup_logging():
    # Custom color scheme for log levels
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

    # Configure logging
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='INFO', logger=logger, fmt='[%(asctime)s] [%(process)d] %(levelname)s %(message)s', level_styles=custom_colors, field_styles=field_styles)

if __name__ == "__main__":
    setup_logging()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="models/v1/model.tflite")
    parser.add_argument("--labels", default="models/v1/labels.txt")

    args = parser.parse_args()

    app = QApplication(sys.argv)
    main_app = App(model_path=args.model, labels_path=args.labels)
    main_app.thread = VideoThreadPiCam()
    main_app.thread.change_pixmap_signal.connect(main_app.update_image)
    main_app.thread.start()
    main_app.show()
    sys.exit(app.exec_())