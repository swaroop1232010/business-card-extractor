"""
Business Card Extractor - Main Application Entry Point
=====================================================

This is the main entry point for the Streamlit application.
It imports and runs the main app from the src directory.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main application
from app import main

if __name__ == "__main__":
    main() 