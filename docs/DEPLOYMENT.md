# Business Card Extractor - Deployment Guide

## Overview
This guide helps you deploy the Business Card Extractor app to various platforms, with special attention to resolving OpenCV installation issues.

## Prerequisites
- Python 3.11+
- Git
- Access to deployment platform (Streamlit Cloud, Heroku, etc.)

## Common Issues and Solutions

### 1. OpenCV Installation Error
**Error**: `ModuleNotFoundError: No module named 'cv2'`

**Solutions**:

#### For Streamlit Cloud:
1. Ensure `packages.txt` includes OpenCV system dependencies
2. Use `opencv-python-headless` instead of `opencv-python` for headless environments
3. The updated `requirements.txt` includes both versions for compatibility

#### For Heroku:
1. Add buildpacks for system dependencies:
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
   ```

2. Create `Aptfile` in root directory:
   ```
   libgl1-mesa-glx
   libglib2.0-0
   libsm6
   libxext6
   libxrender-dev
   libgomp1
   libgthread-2.0-0
   libgtk-3-0
   libavcodec-dev
   libavformat-dev
   libswscale-dev
   libv4l-dev
   libxvidcore-dev
   libx264-dev
   libjpeg-dev
   libpng-dev
   libtiff-dev
   libatlas-base-dev
   gfortran
   ```

#### For Docker:
1. Use a base image with OpenCV dependencies:
   ```dockerfile
   FROM python:3.11-slim
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       libgl1-mesa-glx \
       libglib2.0-0 \
       libsm6 \
       libxext6 \
       libxrender-dev \
       libgomp1 \
       libgthread-2.0-0 \
       libgtk-3-0 \
       libavcodec-dev \
       libavformat-dev \
       libswscale-dev \
       libv4l-dev \
       libxvidcore-dev \
       libx264-dev \
       libjpeg-dev \
       libpng-dev \
       libtiff-dev \
       libatlas-base-dev \
       gfortran \
       && rm -rf /var/lib/apt/lists/*
   
   # Install Python dependencies
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   # Copy application
   COPY . .
   
   # Expose port
   EXPOSE 8501
   
   # Run the app
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

### 2. Database Connection Issues
**Error**: Database connection failures

**Solutions**:
1. Ensure database credentials are properly set as environment variables
2. For cloud databases, whitelist your deployment IP
3. Use connection pooling for better performance

### 3. Memory Issues
**Error**: Out of memory errors during OCR processing

**Solutions**:
1. Increase memory allocation in deployment settings
2. Optimize image processing (already implemented in preprocess.py)
3. Use smaller batch sizes for OCR processing

## Platform-Specific Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy

**Environment Variables**:
```
DATABASE_URL=your_database_connection_string
```

### Heroku
1. Install Heroku CLI
2. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Add buildpacks (see above)
4. Set environment variables:
   ```bash
   heroku config:set DATABASE_URL=your_database_connection_string
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

### Docker
1. Build the image:
   ```bash
   docker build -t business-card-extractor .
   ```
2. Run the container:
   ```bash
   docker run -p 8501:8501 -e DATABASE_URL=your_database_connection_string business-card-extractor
   ```

## Testing Deployment

### 1. Run the Test Script
```bash
python test_opencv.py
```

This will verify:
- OpenCV import
- Basic OpenCV functionality
- Preprocess module import

### 2. Test the Application
1. Upload a sample business card image
2. Verify OCR extraction works
3. Check database storage
4. Test table view functionality

## Troubleshooting

### OpenCV Still Not Working?
1. Try using `opencv-python-headless` only:
   ```bash
   pip uninstall opencv-python
   pip install opencv-python-headless
   ```

2. Check system dependencies:
   ```bash
   ldd $(python -c "import cv2; print(cv2.__file__)")
   ```

3. Verify Python environment:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

### Database Issues?
1. Test connection locally first
2. Check firewall settings
3. Verify connection string format
4. Test with a simple connection script

### Performance Issues?
1. Monitor memory usage
2. Optimize image processing parameters
3. Use connection pooling
4. Implement caching where appropriate

## Support
If you continue to experience issues:
1. Check the logs in your deployment platform
2. Run the test script locally
3. Verify all dependencies are correctly specified
4. Check platform-specific documentation

## Files Modified for Deployment
- `requirements.txt` - Updated with OpenCV compatibility
- `packages.txt` - Added system dependencies for OpenCV
- `runtime.txt` - Specified Python version
- `test_opencv.py` - Created for testing OpenCV installation
- `DEPLOYMENT.md` - This deployment guide 