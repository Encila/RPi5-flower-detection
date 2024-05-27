import sys
import argparse
from PyQt5.QtWidgets import QApplication
from display import App
from video_thread import VideoThreadPiCam

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="models/v1/model.tflite")
    parser.add_argument("--labels", default="models/v1/labels.txt")
    parser.add_argument('--camera_test', action=argparse.BooleanOptionalAction)
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    if args.debug or args.camera_test:
        app = QApplication(sys.argv)
        main_app = App(camera_test_only=args.camera_test, model_path=args.model)
        main_app.thread = VideoThreadPiCam()
        main_app.thread.change_pixmap_signal.connect(main_app.update_image)
        main_app.thread.start()
        main_app.show()
        sys.exit(app.exec_())
    else:
        print("No UI mode not supported with Teachable Machine model.")
