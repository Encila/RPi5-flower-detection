
# RPi5 Flowers Detection

This project utilizes the Raspberry Pi Camera Module 3 on a Raspberry Pi 5 along with TensorFlow Lite and OpenCV to detect and classify flowers using a pre-trained model. The application displays the video feed with annotations using PyQt for visualization.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Model Export](#exporting-the-model-from-teachable-machine)
- [Troubleshooting](#troubleshooting)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Installation

### Prerequisites

Ensure you have the following installed on your Raspberry Pi:

- Python 3.11
- MiniConda
- Pi Camera Module 3

### Using the Setup Script

A `setup.sh` script is provided to automate the installation process. Make sure you have cloned the repository and navigated to its directory.

Run the following command to execute the setup script:

```bash
bash setup.sh
```

### Contents of setup.sh

```bash
#!/bin/bash

# Update and install prerequisites
sudo apt-get update
sudo apt-get install -y cmake python3-libcamera python3-kms++ python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip

# Create conda environment
conda create -n yolov8_picam python=3.11 -y
source ~/miniconda3/etc/profile.d/conda.sh
conda activate yolov8_picam

# Install Python packages from requirements.txt
pip install -r requirements.txt

# Copy necessary libraries to conda environment
sudo cp -r /usr/lib/python3/dist-packages/libcamera ~/miniconda3/envs/yolov8_picam/lib/python3.11/site-packages/
sudo cp -r /usr/lib/python3/dist-packages/pykms ~/miniconda3/envs/yolov8_picam/lib/python3.11/site-packages/

cd ~/miniconda3/envs/yolov8_picam/lib
mv -vf libstdc++.so.6 libstdc++.so.6.old
ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ./libstdc++.so.6

# Install QT5
conda install pyqt -y

echo "Setup complete. Activate the environment using 'conda activate yolov8_picam' and run your scripts."
```

## Usage

### Running the Application

To run the application with the UI:

```bash
python main.py --model=../models/orchidees/model.tflite --debug
```

### Running Exported Models

To run the exported models:

```bash
python main.py --model=./models/yolov8n.onnx --debug
python main.py --model=./models/yolov8n_saved_model/yolov8n_integer_quant.tflite --debug
```

## Exporting the Model from Teachable Machine

To export a model from Teachable Machine:

1. **Train your model** on [Teachable Machine](https://teachablemachine.withgoogle.com/).
2. **Export as TensorFlow Lite**: Click `Export Model` and select `TensorFlow Lite`. Download the model.
3. **Unzip and place the model**: Unzip the downloaded file and move the `.tflite` file to the `models` directory.
4. **Run the application**: Use the path to the new model in your command:

    ```bash
    python main.py --model=./models/your_teachable_machine_model.tflite --debug
    ```

## Troubleshooting

### Common Issues

- **Frozen UI with `cv2.imshow`**: If you encounter issues with the UI freezing, ensure you are using `opencv-python-headless` instead of the regular `opencv-python`.
- **Library Compatibility**: Make sure the libraries are correctly copied to the conda environment and the symbolic link for `libstdc++.so.6` is set up correctly.

## Acknowledgements

This project is inspired by the [RPi5 YOLOv8 Project](https://github.com/JungLearnBot/RPi5_yolov8) and adapted to use TensorFlow Lite for flower detection.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
