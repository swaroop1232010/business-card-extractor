@echo off
REM Business Card Extractor - Deployment Script (Windows)
REM This script helps prepare and deploy the application

echo 🚀 Business Card Extractor - Deployment Preparation
echo ==================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check if required files exist
set required_files=requirements.txt packages.txt runtime.txt app.py
for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo ❌ Missing required file: %%f
        exit /b 1
    ) else (
        echo ✅ Found %%f
    )
)

REM Run deployment test
echo.
echo 🔍 Running deployment tests...
python deployment_test.py
if errorlevel 1 (
    echo ❌ Deployment tests failed. Please fix issues before deploying.
    exit /b 1
) else (
    echo ✅ All deployment tests passed!
)

REM Check git status
echo.
echo 📋 Checking git status...
if exist ".git" (
    git status --porcelain >nul 2>&1
    if errorlevel 1 (
        echo ✅ Working directory is clean
    ) else (
        echo ⚠️ You have uncommitted changes. Consider committing them before deployment.
        git status --short
    )
    
    REM Show current branch
    for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set current_branch=%%i
    echo ✅ Current branch: %current_branch%
) else (
    echo ⚠️ Not a git repository. Consider initializing git for version control.
)

REM Check for environment variables
echo.
echo 🌍 Checking environment variables...
if defined DATABASE_URL (
    echo ✅ DATABASE_URL is set
) else (
    echo ⚠️ DATABASE_URL not set (will use SQLite)
)

REM Deployment platform detection
echo.
echo 🚀 Deployment Platform Detection:

REM Check for Streamlit Cloud
if exist ".streamlit\config.toml" (
    echo ✅ Streamlit Cloud configuration found
)

REM Check for Heroku
if exist "Procfile" (
    echo ✅ Heroku configuration found
) else if exist "app.json" (
    echo ✅ Heroku configuration found
)

REM Check for Docker
if exist "Dockerfile" (
    echo ✅ Docker configuration found
)

REM Provide deployment instructions
echo.
echo 📋 Deployment Instructions:
echo ==========================

if exist ".streamlit\config.toml" (
    echo 🌐 Streamlit Cloud:
    echo    1. Push to GitHub: git push origin main
    echo    2. Go to https://share.streamlit.io
    echo    3. Connect your repository
    echo    4. Set main file path to: app.py
    echo    5. Deploy!
) else if exist "Procfile" (
    echo 🦊 Heroku:
    echo    1. Install Heroku CLI
    echo    2. Run: heroku create your-app-name
    echo    3. Run: git push heroku main
    echo    4. Set environment variables if needed
) else if exist "Dockerfile" (
    echo 🐳 Docker:
    echo    1. Build: docker build -t business-card-extractor .
    echo    2. Run: docker run -p 8501:8501 business-card-extractor
    echo    3. Deploy to your preferred container platform
) else (
    echo 📦 Generic Deployment:
    echo    1. Ensure all dependencies are installed
    echo    2. Set up your deployment platform
    echo    3. Configure environment variables
    echo    4. Deploy the application
)

echo.
echo 🔧 Post-Deployment Checklist:
echo    ✅ App loads without errors
echo    ✅ Image upload works
echo    ✅ OCR extraction functions
echo    ✅ Database operations work
echo    ✅ All features accessible

echo.
echo ✅ Deployment preparation complete!
echo.
echo 📚 For troubleshooting, see: DEPLOYMENT_TROUBLESHOOTING.md
echo 🧪 For testing, run: python deployment_test.py

pause 