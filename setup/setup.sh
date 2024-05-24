#!/bin/bash

# Update and install prerequisites
sudo apt-get update
sudo apt-get install -y cmake

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Conda could not be found, please install Miniconda or Anaconda."
    exit 1
fi

# Create conda environment
conda create -n flower_detection python=3.11 -y

# Ensure conda command is available
source ~/miniconda3/etc/profile.d/conda.sh
conda activate flower_detection

# Install libcamera and PyQt5
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip

# Install libcap for picamera2
sudo apt install -y libcap2 libcap-dev

# Install Python packages from requirements.txt
if [ -f setup/requirements.txt ]; then
    pip install -r setup/requirements.txt
else
    echo "requirements.txt not found."
    exit 1
fi

# Copy necessary libraries to conda environment
sudo cp -r /usr/lib/python3/dist-packages/libcamera ~/miniconda3/envs/flower_detection/lib/python3.11/site-packages/
sudo cp -r /usr/lib/python3/dist-packages/pykms ~/miniconda3/envs/flower_detection/lib/python3.11/site-packages/

# Replace libstdc++ with the system version
cd ~/miniconda3/envs/flower_detection/lib
mv -vf libstdc++.so.6 libstdc++.so.6.old
ln -s /usr/lib/aarch64-linux-gnu/libstdc++.so.6 ./libstdc++.so.6

# Install QT5
conda install pyqt -y

# Replace opencv-python with opencv-python-headless
pip uninstall -y opencv-python
pip install opencv-python-headless==4.6.0.66

cd ~/Desktop/RPi5-flower-detection

echo "Setup complete. Activate the environment using 'conda activate flower_detection' and run your scripts."
