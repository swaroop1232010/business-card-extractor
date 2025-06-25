"""
Virtual Environment Setup Script for Business Card Extraction
This script helps set up a proper Python virtual environment for the project.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    venv_name = "venv"
    
    if Path(venv_name).exists():
        print(f"⚠️ Virtual environment '{venv_name}' already exists")
        response = input("Do you want to recreate it? (y/N): ").lower()
        if response != 'y':
            print("Using existing virtual environment")
            return True
        else:
            print("Removing existing virtual environment...")
            run_command(f"rmdir /s /q {venv_name}", "Removing existing virtual environment")
    
    return run_command(f"python -m venv {venv_name}", "Creating virtual environment")


def activate_virtual_environment():
    """Activate the virtual environment."""
    venv_name = "venv"
    
    if os.name == 'nt':  # Windows
        activate_script = f"{venv_name}\\Scripts\\activate"
        print(f"🔧 To activate the virtual environment, run:")
        print(f"   {venv_name}\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        activate_script = f"{venv_name}/bin/activate"
        print(f"🔧 To activate the virtual environment, run:")
        print(f"   source {venv_name}/bin/activate")
    
    return activate_script


def install_dependencies():
    """Install project dependencies."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")


def main():
    """Main setup function."""
    print("🚀 Business Card Extraction - Virtual Environment Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Get activation script path
    activate_script = activate_virtual_environment()
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("=" * 60)
    
    if os.name == 'nt':  # Windows
        print("1. Activate the virtual environment:")
        print("   venv\\Scripts\\activate")
        print("\n2. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n3. Run the application:")
        print("   streamlit run app.py")
    else:  # Unix/Linux/Mac
        print("1. Activate the virtual environment:")
        print("   source venv/bin/activate")
        print("\n2. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n3. Run the application:")
        print("   streamlit run app.py")
    
    print("\n" + "=" * 60)
    print("💡 Tips:")
    print("- Always activate the virtual environment before running the app")
    print("- If you see 'cv2' errors, make sure you're in the virtual environment")
    print("- The virtual environment keeps your project dependencies isolated")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 