# Deployment Troubleshooting Guide

## 🚨 Common Deployment Issues and Solutions

### 1. OpenCV Import Error
**Error**: `ModuleNotFoundError: No module named 'cv2'`

**Root Cause**: OpenCV system dependencies missing or incompatible version

**Solutions**:

#### For Streamlit Cloud:
1. **Use the updated `packages.txt`** with all OpenCV dependencies
2. **Use `opencv-python-headless`** instead of `opencv-python`
3. **Check Python version** - ensure `runtime.txt` specifies Python 3.11.9

#### For Heroku:
1. Add buildpacks:
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
   ```

2. Create `Aptfile`:
   ```
   libgl1-mesa-glx
   libglib2.0-0
   libsm6
   libxext6
   libxrender-dev
   libgomp1
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
1. **Check environment variables** in deployment platform
2. **Whitelist deployment IP** in database settings
3. **Use connection pooling** for better performance
4. **Test connection locally** first

### 3. Memory Issues
**Error**: Out of memory errors during OCR processing

**Solutions**:
1. **Increase memory allocation** in deployment settings
2. **Optimize image processing** (already implemented)
3. **Use smaller batch sizes** for OCR processing

### 4. Package Version Conflicts
**Error**: Version conflicts between packages

**Solutions**:
1. **Use exact versions** in `requirements.txt`
2. **Test locally** with `deployment_test.py`
3. **Check compatibility** between packages

## 🔧 Pre-Deployment Checklist

### 1. Run Local Tests
```bash
python deployment_test.py
```

This will check:
- ✅ Python version compatibility
- ✅ All critical imports
- ✅ OpenCV functionality
- ✅ Configuration files
- ✅ Database connection
- ✅ Streamlit app import

### 2. Verify Configuration Files

#### `requirements.txt`:
- [ ] All packages have exact versions (==)
- [ ] No conflicting version ranges
- [ ] OpenCV packages included
- [ ] All dependencies listed

#### `packages.txt`:
- [ ] No duplicate packages
- [ ] All OpenCV dependencies included
- [ ] No invalid package names
- [ ] No comments that might cause issues

#### `runtime.txt`:
- [ ] Python version specified (3.11.9)
- [ ] No extra whitespace or characters

### 3. Test Dependencies Locally
```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test imports
python -c "import cv2; print('OpenCV OK')"
python -c "import streamlit; print('Streamlit OK')"
python -c "import easyocr; print('EasyOCR OK')"
```

## 🚀 Deployment Best Practices

### 1. Streamlit Cloud
1. **Push to GitHub** with all configuration files
2. **Connect repository** to Streamlit Cloud
3. **Set environment variables** if using external database
4. **Monitor deployment logs** for errors

### 2. Heroku
1. **Add buildpacks** for system dependencies
2. **Set environment variables**:
   ```bash
   heroku config:set DATABASE_URL=your_connection_string
   ```
3. **Scale dyno** if needed for memory

### 3. Docker
1. **Build image locally** first:
   ```bash
   docker build -t business-card-extractor .
   ```
2. **Test container**:
   ```bash
   docker run -p 8501:8501 business-card-extractor
   ```
3. **Push to registry** and deploy

## 🐛 Troubleshooting Steps

### Step 1: Check Deployment Logs
1. **Streamlit Cloud**: Click "Manage app" → "Logs"
2. **Heroku**: `heroku logs --tail`
3. **Docker**: `docker logs container_name`

### Step 2: Identify the Issue
Common error patterns:
- `ModuleNotFoundError`: Missing Python package
- `ImportError`: System dependency missing
- `ConnectionError`: Database connectivity issue
- `MemoryError`: Insufficient memory allocation

### Step 3: Apply Fixes
1. **Update configuration files** based on error
2. **Test locally** with `deployment_test.py`
3. **Redeploy** with fixes
4. **Monitor logs** for resolution

### Step 4: Verify Fix
1. **Check app loads** without errors
2. **Test core functionality** (upload image, extract data)
3. **Verify database operations** work
4. **Monitor performance** and memory usage

## 📋 Emergency Fixes

### Quick OpenCV Fix
If OpenCV still fails, try this minimal `requirements.txt`:
```
streamlit==1.31.0
opencv-python-headless==4.8.1.78
pandas==2.2.0
numpy==1.26.4
Pillow==10.2.0
easyocr==1.7.1
sqlalchemy==2.0.30
```

### Minimal packages.txt
```
libgl1-mesa-glx
libglib2.0-0
libsm6
libxext6
libjpeg-dev
libpng-dev
libpq-dev
```

### Database Fallback
If external database fails, the app will automatically use SQLite.

## 🔍 Debugging Tools

### 1. Deployment Test Script
```bash
python deployment_test.py
```

### 2. Manual Import Test
```bash
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import cv2
    print(f'OpenCV: {cv2.__version__}')
except ImportError as e:
    print(f'OpenCV Error: {e}')
"
```

### 3. System Information
```bash
python -c "
import platform
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.architecture()}')
print(f'Machine: {platform.machine()}')
"
```

## 📞 Getting Help

### 1. Check Documentation
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Docker Documentation](https://docs.docker.com/)

### 2. Common Issues Repository
- [OpenCV Installation Issues](https://github.com/opencv/opencv/issues)
- [Streamlit Deployment Issues](https://github.com/streamlit/streamlit/issues)

### 3. Community Support
- [Streamlit Community](https://discuss.streamlit.io/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/streamlit)

## 🎯 Success Metrics

Your deployment is successful when:
- ✅ App loads without errors
- ✅ Image upload works
- ✅ OCR extraction functions
- ✅ Database operations work
- ✅ All features accessible
- ✅ Performance is acceptable

## 📈 Monitoring

After successful deployment:
1. **Monitor app performance**
2. **Check error logs regularly**
3. **Monitor database connections**
4. **Track user interactions**
5. **Update dependencies periodically**

---

**Remember**: Always test locally first, use the deployment test script, and monitor logs during deployment! 