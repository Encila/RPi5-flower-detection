#!/bin/bash

# Update and install prerequisites
sudo apt-get update
sudo apt-get install -y cmake

# Create conda environment
conda create -n flower_detection python=3.11 -y

# Ensure conda command is available
source ~/miniconda3/etc/profile.d/conda.sh
conda activate flower_detection

# Install libcamera and PyQt5
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip

# Install Python packages from requirements.txt
pip install -r setup/requirements.txt

# Copy necessary libraries to conda environment
sudo cp -r /usr/lib/python3/dist-packages/libcamera ~/miniconda3/envs/flower_detection/lib/python3.11/site-packages/
sudo cp -r /usr/lib/python3/dist-packages/pykms ~/miniconda3/envs/flower_detection/lib/python3.11/site-packages/

# Replace libstdc++ with the system version
cd ~/miniconda3/envs/flower_detection/lib
mv -vf libstdc++.so.6 libstdc++.so.6.old
ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ./libstdc++.so.6

# Install QT5
conda install pyqt -y

# Replace opencv-python with opencv-python-headless
pip uninstall -y opencv-python
pip install opencv-python-headless==4.6.0.66

# Go back to the directory
cd ~/Desktop/RPi5-flower-detection

echo Setup complete. Activate the environment using 'conda activate flower_detection' and run your scripts.
