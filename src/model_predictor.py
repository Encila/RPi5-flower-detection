import tensorflow as tf
import numpy as np
import cv2
import logging

class ModelPredictor:
    """
    A class to handle model predictions.

    Attributes:
    model_path (str): Path to the model file.
    labels_path (str): Path to the labels file.
    """
    def __init__(self, model_path, labels_path):
        self.interpreter = self.load_model(model_path)
        self.labels = self.load_labels(labels_path)

    def load_model(self, model_path):
        try:
            interpreter = tf.lite.Interpreter(model_path=str(model_path))
            interpreter.allocate_tensors()
            return interpreter
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise

    def load_labels(self, labels_path):
        try:
            with open(labels_path, 'r') as file:
                labels = {i: line.strip() for i, line in enumerate(file.readlines())}
            return labels
        except Exception as e:
            logging.error(f"Failed to load labels: {e}")
            raise

    def predict(self, frame):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        input_shape = input_details[0]['shape']
        logging.debug(f"input_shape -> {input_shape}")

        if len(input_shape) != 4 or input_shape[0] != 1:
            raise ValueError(f"Unexpected input_shape: {input_shape}")

        frame = (cv2.resize(frame, (input_shape[2], input_shape[1])) / 255.0).astype(np.uint8)   # Normalize the image
        frame = np.expand_dims(frame, axis=0)
        self.interpreter.set_tensor(input_details[0]['index'], frame)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])[0]
        probabilities = tf.nn.softmax(output_data).numpy()
        class_id = np.argmax(probabilities)
        confidence = probabilities[class_id]
        logging.debug(f"output_data -> {output_data}")
        return class_id, confidence
