import sys
import argparse
from PyQt5.QtWidgets import QApplication
from display import App
from video_thread import VideoThreadPiCam

if __name__ == "__main__":
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

