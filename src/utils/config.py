"""
Configuration utilities for the GoDaddy Domain Management tool.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Set up and configure the application logger."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger("domain_manager")
    logger.setLevel(logging.INFO)
    
    # Create handlers
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "domain_manager.log"),
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=5
    )
    console_handler = logging.StreamHandler()
    
    # Set levels
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    
    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    
    # Add formatters to handlers
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 