#!/bin/bash

# Update package list and upgrade pip
echo "Updating package list and upgrading pip..."
sudo apt update -y
sudo apt install --upgrade python3-pip -y

# Check if virtualenv is installed
echo "Checking for virtualenv..."
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv not found, installing it..."
    sudo apt install python3-venv -y
else
    echo "virtualenv is already installed."
fi

# Create and activate a virtual environment
echo "Creating a virtual environment..."
python3 -m venv myenv

# Activate the virtual environment
echo "Activating the virtual environment..."
source myenv/bin/activate

# Upgrade pip inside the virtual environment
echo "Upgrading pip inside the virtual environment..."
pip install --upgrade pip

# Install Gunicorn
echo "Installing Gunicorn..."
pip install gunicorn

# Check if the installation was successful
if command -v gunicorn &> /dev/null; then
    echo "Gunicorn installed successfully!"
else
    echo "Gunicorn installation failed."
fi

# Deactivate virtual environment after installation
deactivate
echo "Virtual environment deactivated."
