#!/usr/bin/env python3
"""
Test script to validate packages.txt file
"""

def validate_packages():
    """Validate the packages.txt file."""
    print("🔍 Validating packages.txt...")
    
    # Read packages.txt
    try:
        with open('packages.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ packages.txt not found")
        return False
    
    # Extract package names (skip comments and empty lines)
    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            packages.append(line)
    
    print(f"📦 Found {len(packages)} packages:")
    for pkg in packages:
        print(f"   ✅ {pkg}")
    
    # Check for duplicates
    duplicates = [pkg for pkg in set(packages) if packages.count(pkg) > 1]
    if duplicates:
        print(f"⚠️ Duplicate packages found: {duplicates}")
        return False
    
    print("✅ packages.txt validation passed!")
    return True

if __name__ == "__main__":
    validate_packages() 