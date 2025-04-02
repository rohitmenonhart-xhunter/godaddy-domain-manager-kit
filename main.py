#!/usr/bin/env python3
"""
GoDaddy Domain Management Automation Tool

This script automates the process of checking domain availability and purchasing domains
through the GoDaddy API.
"""

import os
import sys
from dotenv import load_dotenv
from src.ui.cli import DomainCLI
from src.api.godaddy_client import GoDaddyClient
from src.utils.config import setup_logger

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    # Setup logger
    logger = setup_logger()
    
    # Check for API credentials
    api_key = os.getenv("GODADDY_API_KEY")
    api_secret = os.getenv("GODADDY_API_SECRET")
    
    if not api_key or not api_secret or api_key == "your_api_key_here":
        logger.error("GoDaddy API credentials not found or not updated in .env file")
        print("Error: Please update your GoDaddy API credentials in the .env file")
        sys.exit(1)
    
    # Initialize GoDaddy client
    api_url = os.getenv("API_URL", "https://api.godaddy.com")
    godaddy_client = GoDaddyClient(api_key, api_secret, api_url)
    
    # Initialize CLI interface
    cli = DomainCLI(godaddy_client)
    
    # Start the domain management flow
    cli.start()

if __name__ == "__main__":
    main() 