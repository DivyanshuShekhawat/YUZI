#!/usr/bin/env bash
# Install system dependencies required by pyaudio and other packages
apt-get update
apt-get install -y portaudio19-dev python3-pyaudio libasound2-dev libx11-dev libxtst-dev libjpeg-dev libpng-dev libxcb1-dev

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt 