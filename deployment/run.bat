@echo off
echo 🚀 Starting Business Card Extraction App...
echo ==========================================

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Virtual environment not found
    echo Please run setup.bat first to create the virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist app.py (
    echo ❌ app.py not found
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)

REM Run the Streamlit app using the virtual environment's Python
echo 🎯 Starting Streamlit application...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
venv\Scripts\python.exe -m streamlit run app.py

pause 