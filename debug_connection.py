#!/usr/bin/env python3
"""
Debug script to test Supabase connection and identify issues
"""

import os
import sys
import socket

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_network_connectivity():
    """Test basic network connectivity to Supabase."""
    print("🔍 Testing network connectivity...")
    
    host = "db.ncjbnmsvthkttatdwdaz.supabase.co"
    port = 5432
    
    try:
        # Test DNS resolution
        print(f"📡 Resolving DNS for {host}...")
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolved: {host} -> {ip}")
        
        # Test TCP connection
        print(f"🔌 Testing TCP connection to {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ TCP connection successful to {host}:{port}")
        else:
            print(f"❌ TCP connection failed to {host}:{port} (error code: {result})")
            
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
    except Exception as e:
        print(f"❌ Network test failed: {e}")

def test_environment_variables():
    """Check if environment variables are set correctly."""
    print("\n🔍 Checking environment variables...")
    
    env_vars = [
        "SUPABASE_HOST",
        "SUPABASE_PORT", 
        "SUPABASE_USER",
        "SUPABASE_PASSWORD",
        "SUPABASE_DB"
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Mask password for security
            if "PASSWORD" in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def test_database_connection():
    """Test the actual database connection."""
    print("\n🔍 Testing database connection...")
    
    try:
        from config.config import get_supabase_db_config
        from core.database import set_db_config, db_manager
        
        # Get configuration
        config = get_supabase_db_config()
        print(f"📋 Configuration: {config}")
        
        # Test connection
        success = set_db_config(*config)
        if success:
            print("✅ Database configuration set successfully")
            
            if db_manager.test_connection():
                print("✅ Database connection test successful")
            else:
                print("❌ Database connection test failed")
        else:
            print("❌ Failed to set database configuration")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting connection debug...")
    test_network_connectivity()
    test_environment_variables()
    test_database_connection()
    print("\n🎉 Debug complete!") 