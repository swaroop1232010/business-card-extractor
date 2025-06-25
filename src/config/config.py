"""
Configuration Settings for Business Card Extractor
=================================================

This module contains all configuration settings for the application.
"""

import os
from typing import Dict, Any

# Supabase Configuration - Use environment variables with defaults for deployment
SUPABASE_DEFAULTS = {
    "host": os.environ.get("SUPABASE_HOST", "db.ncjbnmsvthkttatdwdaz.supabase.co"),
    "port": os.environ.get("SUPABASE_PORT", "5432"),
    "user": os.environ.get("SUPABASE_USER", "postgres"),
    "password": os.environ.get("SUPABASE_PASSWORD", "fmv_v7UjDN+&Td&"),
    "database": os.environ.get("SUPABASE_DB", "postgres")
}

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

def get_supabase_db_config() -> tuple:
    """Get database configuration with Supabase defaults for deployment."""
    return (
        "postgresql",
        SUPABASE_DEFAULTS["host"],
        SUPABASE_DEFAULTS["user"],
        SUPABASE_DEFAULTS["password"],
        SUPABASE_DEFAULTS["database"],
        SUPABASE_DEFAULTS["port"],
        None
    )

def is_production() -> bool:
    """Check if running in production environment."""
    return os.environ.get("STREAMLIT_SERVER_ENV") == "production"

def get_deployment_info() -> Dict[str, Any]:
    """Get deployment information."""
    return {
        "environment": "production" if is_production() else "development",
        "database": "Supabase" if is_production() else "Local",
        "supabase_host": SUPABASE_DEFAULTS["host"],
        "supabase_user": SUPABASE_DEFAULTS["user"]
    } 