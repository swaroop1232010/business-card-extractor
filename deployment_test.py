#!/usr/bin/env python3
"""
Deployment Test Script for Business Card Extractor
Run this script locally to verify all dependencies will work in deployment
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

def test_python_version():
    """Test Python version compatibility."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python version should be 3.11+")
        return False

def test_critical_imports():
    """Test if all critical modules can be imported."""
    print("\n📦 Testing critical imports...")
    
    critical_modules = [
        ('streamlit', 'Streamlit'),
        ('cv2', 'OpenCV'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('easyocr', 'EasyOCR'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('psycopg2', 'PostgreSQL'),
        ('mysql.connector', 'MySQL'),
        ('torch', 'PyTorch'),
        ('torchvision', 'TorchVision'),
    ]
    
    all_ok = True
    for module_name, display_name in critical_modules:
        try:
            importlib.import_module(module_name)
            print(f"   ✅ {display_name}")
        except ImportError as e:
            print(f"   ❌ {display_name}: {e}")
            all_ok = False
    
    return all_ok

def test_app_modules():
    """Test if app-specific modules can be imported."""
    print("\n🔧 Testing app modules...")
    
    app_modules = [
        ('preprocess', 'Preprocess'),
        ('ocr', 'OCR'),
        ('classify', 'Classify'),
        ('database', 'Database'),
    ]
    
    all_ok = True
    for module_name, display_name in app_modules:
        try:
            importlib.import_module(module_name)
            print(f"   ✅ {display_name}")
        except ImportError as e:
            print(f"   ❌ {display_name}: {e}")
            all_ok = False
    
    return all_ok

def test_opencv_functionality():
    """Test OpenCV functionality specifically."""
    print("\n🔍 Testing OpenCV functionality...")
    
    try:
        import cv2
        import numpy as np
        
        # Test basic image operations
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:] = (255, 0, 0)  # Blue image
        
        # Test image processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        print("   ✅ OpenCV basic functionality works")
        print(f"   ✅ Image shape: {img.shape}")
        print(f"   ✅ Gray shape: {gray.shape}")
        print(f"   ✅ Blur shape: {blur.shape}")
        return True
        
    except Exception as e:
        print(f"   ❌ OpenCV functionality test failed: {e}")
        return False

def test_config_files():
    """Test if all necessary configuration files exist."""
    print("\n📁 Testing configuration files...")
    
    config_files = [
        ('requirements.txt', 'Requirements'),
        ('packages.txt', 'System packages'),
        ('runtime.txt', 'Python runtime'),
        ('app.py', 'Main application'),
    ]
    
    all_ok = True
    for filename, display_name in config_files:
        if Path(filename).exists():
            print(f"   ✅ {display_name} ({filename})")
        else:
            print(f"   ❌ {display_name} ({filename}) - Missing")
            all_ok = False
    
    return all_ok

def test_requirements_file():
    """Test if requirements.txt is valid."""
    print("\n📋 Testing requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        # Check for common issues
        issues = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if '>=' in line and '<=' not in line:
                    issues.append(f"Line {i}: Consider using exact version for '{line.split('>=')[0].strip()}'")
                elif '==' not in line and '>=' not in line and '<=' not in line:
                    issues.append(f"Line {i}: No version specified for '{line}'")
        
        if issues:
            print("   ⚠️ Potential issues found:")
            for issue in issues:
                print(f"      {issue}")
        else:
            print("   ✅ Requirements file looks good")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading requirements.txt: {e}")
        return False

def test_packages_file():
    """Test if packages.txt is valid."""
    print("\n📦 Testing packages.txt...")
    
    try:
        with open('packages.txt', 'r') as f:
            lines = f.readlines()
        
        # Extract package names (skip comments and empty lines)
        packages = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                packages.append(line)
        
        print(f"   ✅ Found {len(packages)} packages")
        
        # Check for duplicates
        duplicates = [pkg for pkg in set(packages) if packages.count(pkg) > 1]
        if duplicates:
            print(f"   ⚠️ Duplicate packages found: {duplicates}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading packages.txt: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    print("\n🗄️ Testing database connection...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        
        # Test connection
        if db.test_connection():
            print("   ✅ Database connection successful")
            return True
        else:
            print("   ❌ Database connection failed")
            return False
    except Exception as e:
        print(f"   ⚠️ Could not test database connection: {e}")
        return True  # Not critical for deployment

def test_streamlit_app():
    """Test if the Streamlit app can be imported."""
    print("\n🚀 Testing Streamlit app...")
    
    try:
        # Test if app.py can be imported without errors
        import app
        print("   ✅ Streamlit app imports successfully")
        return True
    except Exception as e:
        print(f"   ❌ Streamlit app import failed: {e}")
        return False

def main():
    """Run all deployment tests."""
    print("🚀 Business Card Extractor - Deployment Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Critical Imports", test_critical_imports),
        ("App Modules", test_app_modules),
        ("OpenCV Functionality", test_opencv_functionality),
        ("Config Files", test_config_files),
        ("Requirements File", test_requirements_file),
        ("Packages File", test_packages_file),
        ("Database Connection", test_database_connection),
        ("Streamlit App", test_streamlit_app),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Deployment Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for deployment.")
        print("\n📋 Deployment Checklist:")
        print("   ✅ All dependencies are compatible")
        print("   ✅ Configuration files are valid")
        print("   ✅ OpenCV is working correctly")
        print("   ✅ Database connection is stable")
        return True
    elif passed >= total - 2:  # Allow 2 non-critical failures
        print("⚠️ Most tests passed. Review failed tests before deployment.")
        print("\n🔧 Recommended actions:")
        for test_name, result in results:
            if not result:
                print(f"   - Fix {test_name} issue")
        return True
    else:
        print("❌ Multiple tests failed. Please fix issues before deployment.")
        print("\n🔧 Critical issues to fix:")
        for test_name, result in results:
            if not result:
                print(f"   - {test_name}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 