#!/bin/bash

# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python & Pip
sudo apt install python3 python3-pip -y

# Create and activate virtualenv (necessary for ubuntu 22.04+)
python3 -m venv stylescout-env
source stylescout-env/bin/activate

# Install Playwright for browser automation
pip install --upgrade pip
pip install playwright
playwright install
playwright install-deps

# Install Google Vision API client
pip install google-cloud-vision

# Install requests for API calls
pip install requests

# Install cron for automation
sudo apt install cron -y
