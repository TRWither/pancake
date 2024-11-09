#!/usr/bin/bash

set -e

echo "Installing PanCake version 1.0.0..."

# Check if Python3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python3 is not installed. Stopping installation..."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 >/dev/null 2>&1; then
    echo "pip3 is not installed."
    echo "Installing pip3..."
    python3 -m ensurepip --upgrade
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "No virtual environment found."
    echo "Creating a virtual environment..."
    python3 -m venv pancake-venv
fi

# Activate virtual environemnt
echo "Activating virtual environment..."
source pancake-venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create command
SCRIPT_DIR=$(dirname "$(realpath "$0")")

if [ ! -f "$SCRIPT_DIR/PanCake.py" ]; then
    echo "ERROR: PanCake.py not found in the current directory ($SCRIPT_DIR)."
    exit 1
fi

chmod +x "$SCRIPT_DIR/PanCake.py"
mv "$SCRIPT_DIR/PanCake.py" /usr/local/bin/pancake

echo "PanCake successfully installed!"
echo "Type 'source pancake-venv/bin/activate' to activate the virtual environment"