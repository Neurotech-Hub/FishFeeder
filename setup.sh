#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

echo "Setup complete! To activate the virtual environment, run: source venv/bin/activate" 