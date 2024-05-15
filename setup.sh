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
