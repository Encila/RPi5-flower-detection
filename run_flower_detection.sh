#!/bin/bash

# Activate the conda environment
echo "Activating conda environment"
source /home/fablabensfea/miniconda3/etc/profile.d/conda.sh
conda activate flower_detection

# Verify the exit status of the conda command
if [ $? -ne 0 ]; then
    echo "Failed to activate conda environment"
    exit 1
fi

# Move to the directory where the Python script is located
echo "Changing directory to ~/Desktop/RPi5-flower-detection"
cd ~/Desktop/RPi5-flower-detection

# Execute the Python script
python src/main.py

# Verify the exit status of the Python script
if [ $? -ne 0 ]; then
    echo "Python script failed to run"
    exit 1
fi

echo "Script executed successfully"