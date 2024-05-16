#!/bin/bash

# Function to print and execute a command
run_command() {
  echo "Running: $1"
  eval $1
  if [ $? -ne 0 ]; then
    echo "Command failed: $1"
    exit 1
  fi
}

# Update and install prerequisites
run_command "sudo apt-get update"
run_command "sudo apt-get install -y cmake"

# Create conda environment
run_command "conda create -n flower_detection python=3.11 -y"

# Ensure conda command is available
run_command "source ~/miniconda3/etc/profile.d/conda.sh"
run_command "conda activate flower_detection"

# Install libcamera and PyQt5
run_command "sudo apt install -y python3-libcamera python3-kms++"
run_command "sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip"

# Install Python packages from requirements.txt
run_command "pip install -r requirements.txt"

# Copy necessary libraries to conda environment
run_command "sudo cp -r /usr/lib/python3/dist-packages/libcamera ~/miniconda3/envs/flower_detection/lib/python3.11/site-packages/"
run_command "sudo cp -r /usr/lib/python3/dist-packages/pykms ~/miniconda3/envs/flower_detection/lib/python3.11/site-packages/"

# Replace libstdc++ with the system version
cd ~/miniconda3/envs/flower_detection/lib
run_command "mv -vf libstdc++.so.6 libstdc++.so.6.old"
run_command "ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ./libstdc++.so.6"

# Install QT5
run_command "conda install pyqt -y"

# Replace opencv-python with opencv-python-headless
run_command "pip uninstall -y opencv-python"
run_command "pip install opencv-python-headless==4.6.0.66"

echo "Setup complete. Activate the environment using 'conda activate flower_detection' and run your scripts."
