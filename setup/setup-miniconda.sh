#!/bin/bash

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda.sh
bash ~/miniconda.sh
source ~/miniconda3/etc/profile.d/conda.sh
conda init bash
conda --version
