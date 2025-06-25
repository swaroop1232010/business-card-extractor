"""
Test script to verify installation and module imports.
Run this script to check if all dependencies are properly installed.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    
    required_modules = [
        'streamlit',
        'opencv-python',
        'easyocr',
        'mysql.connector',
        'pandas',
        'numpy',
        'PIL'
    ]
    
    print("🔍 Testing module imports...")
    print("=" * 50)
    
    all_imports_successful = True
    
    for module in required_modules:
        try:
            if module == 'opencv-python':
                importlib.import_module('cv2')
                print(f"✅ {module} (cv2)")
            elif module == 'PIL':
                importlib.import_module('PIL')
                print(f"✅ {module} (PIL)")
            else:
                importlib.import_module(module)
                print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_imports_successful = False
    
    print("=" * 50)
    
    if all_imports_successful:
        print("🎉 All required modules imported successfully!")
    else:
        print("⚠️  Some modules failed to import. Please check your installation.")
    
    return all_imports_successful


def test_custom_modules():
    """Test if custom modules can be imported."""
    
    custom_modules = [
        'preprocess',
        'ocr',
        'classify',
        'database'
    ]
    
    print("\n🔍 Testing custom module imports...")
    print("=" * 50)
    
    all_custom_imports_successful = True
    
    for module in custom_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}.py")
        except ImportError as e:
            print(f"❌ {module}.py: {e}")
            all_custom_imports_successful = False
    
    print("=" * 50)
    
    if all_custom_imports_successful:
        print("🎉 All custom modules imported successfully!")
    else:
        print("⚠️  Some custom modules failed to import.")
    
    return all_custom_imports_successful


def test_directories():
    """Test if required directories exist."""
    
    import os
    from pathlib import Path
    
    print("\n🔍 Testing directory structure...")
    print("=" * 50)
    
    required_dirs = ['temp']
    all_dirs_exist = True
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_dirs_exist = False
    
    print("=" * 50)
    
    if all_dirs_exist:
        print("🎉 All required directories exist!")
    else:
        print("⚠️  Some directories are missing.")
    
    return all_dirs_exist


def test_files():
    """Test if required files exist."""
    
    import os
    from pathlib import Path
    
    print("\n🔍 Testing required files...")
    print("=" * 50)
    
    required_files = [
        'app.py',
        'preprocess.py',
        'ocr.py',
        'classify.py',
        'database.py',
        'requirements.txt',
        'setup.sql',
        'README.md'
    ]
    
    all_files_exist = True
    
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name}")
            all_files_exist = False
    
    print("=" * 50)
    
    if all_files_exist:
        print("🎉 All required files exist!")
    else:
        print("⚠️  Some files are missing.")
    
    return all_files_exist


def main():
    """Main test function."""
    
    print("🚀 Business Card Extraction - Installation Test")
    print("=" * 60)
    
    # Test all components
    imports_ok = test_imports()
    custom_imports_ok = test_custom_modules()
    dirs_ok = test_directories()
    files_ok = test_files()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    print(f"Module Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Custom Modules: {'✅ PASS' if custom_imports_ok else '❌ FAIL'}")
    print(f"Directories: {'✅ PASS' if dirs_ok else '❌ FAIL'}")
    print(f"Files: {'✅ PASS' if files_ok else '❌ FAIL'}")
    
    overall_success = imports_ok and custom_imports_ok and dirs_ok and files_ok
    
    print("=" * 60)
    
    if overall_success:
        print("🎉 All tests passed! Your installation is ready.")
        print("\n📋 Next steps:")
        print("1. Set up MySQL database using setup.sql")
        print("2. Configure database credentials")
        print("3. Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before proceeding.")
        print("\n🔧 Common fixes:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check if all files are in the correct directory")
        print("3. Ensure Python version is 3.8 or higher")
    
    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 