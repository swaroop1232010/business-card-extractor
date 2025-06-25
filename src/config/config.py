"""
Configuration Settings for Business Card Extractor (SQLite only)
=================================================

This module contains all configuration settings for the application.
"""

import os
from typing import Dict, Any

# SQLite Configuration
DB_PATH = os.environ.get("SQLITE_DB_PATH", "business_cards.db")

# Application Settings
APP_CONFIG = {
    "page_title": "Business Card Extractor Pro",
    "page_icon": "📇",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://github.com/your-repo/business-card-extractor',
        'Report a bug': 'https://github.com/your-repo/business-card-extractor/issues',
        'About': 'Business Card Extractor Pro - AI-powered OCR for business cards'
    }
}

# File Upload Settings
UPLOAD_CONFIG = {
    "allowed_types": ['jpg', 'jpeg', 'png'],
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "temp_dir": "temp"
}

# Database Settings
DB_CONFIG = {
    "table_name": "business_cards",
    "cache_ttl": 60,  # seconds
    "max_contacts_per_page": 100
}

# OCR Settings
OCR_CONFIG = {
    "confidence_threshold": 0.5,
    "language": "en"
}

def get_sqlite_db_config() -> str:
    """Get SQLite database file path."""
    return DB_PATH

def get_deployment_info() -> Dict[str, Any]:
    """Get deployment information."""
    return {
        "environment": "production" if os.environ.get("STREAMLIT_SERVER_ENV") == "production" else "development",
        "database": f"SQLite ({DB_PATH})"
    } 