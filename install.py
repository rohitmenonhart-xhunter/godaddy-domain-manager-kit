#!/usr/bin/env python3
"""
Installation script for the GoDaddy Domain Management Tool.

This script sets up the application by:
1. Activating the virtual environment
2. Installing dependencies
3. Creating necessary directories
4. Generating an initial .env file if it doesn't exist
"""

import os
import sys
import subprocess
import platform

def main():
    """Main installation function."""
    print("=" * 80)
    print("GoDaddy Domain Management Tool - Installation")
    print("=" * 80)
    
    # Determine OS and virtual environment activation command
    is_windows = platform.system().lower() == "windows"
    venv_activate = os.path.join("venv", "Scripts", "activate") if is_windows else os.path.join("venv", "bin", "activate")
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError:
            print("Error: Failed to create virtual environment.")
            return False
    
    # Install dependencies
    print("Installing dependencies...")
    
    pip_cmd = [
        "venv\\Scripts\\pip.exe" if is_windows else "./venv/bin/pip",
        "install", "-r", "requirements.txt"
    ]
    
    try:
        subprocess.check_call(pip_cmd)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
        return False
    
    # Create necessary directories
    print("Creating necessary directories...")
    os.makedirs("logs", exist_ok=True)
    
    # Create initial .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("Creating initial .env file...")
        with open(".env", "w") as f:
            f.write("""# GoDaddy API Credentials
GODADDY_API_KEY=your_api_key_here
GODADDY_API_SECRET=your_api_secret_here

# Environment Settings
API_URL=https://api.godaddy.com
# Uncomment for test environment
# API_URL=https://api.ote-godaddy.com
""")
        print("Created .env file. Please update it with your API credentials.")
    else:
        print(".env file already exists.")
    
    print("\nInstallation completed!")
    print("\nTo start using the application:")
    
    if is_windows:
        print("1. Activate the virtual environment: venv\\Scripts\\activate")
    else:
        print("1. Activate the virtual environment: source venv/bin/activate")
    
    print("2. Update your GoDaddy API credentials in the .env file")
    print("3. Run the application: python main.py")
    print("\nEnjoy using the GoDaddy Domain Management Tool!")
    
    return True

if __name__ == "__main__":
    main() 