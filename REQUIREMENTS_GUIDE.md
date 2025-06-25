# Requirements Files Guide

## 📋 Available Requirements Files

### 1. `requirements.txt` (Recommended)
**Use for**: Standard deployment with Python 3.13
**Features**:
- Flexible version ranges (`>=`) for Python 3.13 compatibility
- Removed problematic packages (sympy, ninja)
- Uses `opencv-python-headless` for deployment
- Conservative but complete dependency set

### 2. `requirements_minimal.txt` (Fallback)
**Use for**: When standard requirements cause issues
**Features**:
- Only essential packages
- Minimal dependencies
- Good for troubleshooting

### 3. `requirements_conservative.txt` (Ultra-Safe)
**Use for**: Maximum compatibility, minimal features
**Features**:
- Very few dependencies
- Only core functionality
- Best for Python 3.13 compatibility

## 🚀 When to Use Each File

### For Streamlit Cloud with Python 3.13
```bash
# Try this first
requirements.txt

# If that fails, try this
requirements_minimal.txt

# If still having issues, use this
requirements_conservative.txt
```

### For Local Development
```bash
# Use standard requirements
pip install -r requirements.txt
```

### For Production Deployment
```bash
# Start with conservative approach
pip install -r requirements_conservative.txt

# Gradually add more packages as needed
```

## 🔧 Quick Fixes

### If PyTorch Fails
```bash
# Replace in requirements.txt
torch>=2.2.0
torchvision>=0.17.0
```

### If OpenCV Fails
```bash
# Use headless version only
opencv-python-headless>=4.8.0
```

### If Database Connectors Fail
```bash
# Use binary versions
psycopg2-binary>=2.9.9
```

## 📊 Package Comparison

| Package | Standard | Minimal | Conservative |
|---------|----------|---------|--------------|
| streamlit | ✅ | ✅ | ✅ |
| pandas | ✅ | ✅ | ✅ |
| numpy | ✅ | ✅ | ✅ |
| opencv-python-headless | ✅ | ✅ | ✅ |
| easyocr | ✅ | ✅ | ✅ |
| torch | ✅ | ✅ | ✅ |
| torchvision | ✅ | ✅ | ✅ |
| sqlalchemy | ✅ | ✅ | ✅ |
| psycopg2-binary | ✅ | ✅ | ✅ |
| mysql-connector-python | ✅ | ✅ | ✅ |
| scipy | ✅ | ✅ | ✅ |
| scikit-image | ✅ | ✅ | ✅ |
| openpyxl | ✅ | ✅ | ✅ |
| altair | ✅ | ✅ | ✅ |
| protobuf | ✅ | ✅ | ✅ |
| pyarrow | ✅ | ✅ | ✅ |
| requests | ✅ | ✅ | ✅ |
| rich | ✅ | ✅ | ✅ |
| jinja2 | ✅ | ✅ | ✅ |
| jsonschema | ✅ | ✅ | ✅ |
| python-bidi | ✅ | ❌ | ❌ |
| PyYAML | ✅ | ❌ | ❌ |
| Shapely | ✅ | ❌ | ❌ |
| pyclipper | ✅ | ❌ | ❌ |
| blinker | ✅ | ❌ | ❌ |
| cachetools | ✅ | ❌ | ❌ |
| click | ✅ | ❌ | ❌ |
| gitpython | ✅ | ❌ | ❌ |
| importlib-metadata | ✅ | ❌ | ❌ |
| packaging | ✅ | ❌ | ❌ |
| python-dateutil | ✅ | ❌ | ❌ |
| toml | ✅ | ❌ | ❌ |
| tornado | ✅ | ❌ | ❌ |
| watchdog | ✅ | ❌ | ❌ |
| pytz | ✅ | ❌ | ❌ |
| tzdata | ✅ | ❌ | ❌ |
| toolz | ✅ | ❌ | ❌ |
| colorama | ✅ | ❌ | ❌ |
| gitdb | ✅ | ❌ | ❌ |
| zipp | ✅ | ❌ | ❌ |
| six | ✅ | ❌ | ❌ |
| charset-normalizer | ✅ | ❌ | ❌ |
| idna | ✅ | ❌ | ❌ |
| urllib3 | ✅ | ❌ | ❌ |
| certifi | ✅ | ❌ | ❌ |
| markdown-it-py | ✅ | ❌ | ❌ |
| pygments | ✅ | ❌ | ❌ |
| filelock | ✅ | ❌ | ❌ |
| networkx | ✅ | ❌ | ❌ |
| fsspec | ✅ | ❌ | ❌ |
| imageio | ✅ | ❌ | ❌ |
| tifffile | ✅ | ❌ | ❌ |
| lazy-loader | ✅ | ❌ | ❌ |
| smmap | ✅ | ❌ | ❌ |
| MarkupSafe | ✅ | ❌ | ❌ |
| attrs | ✅ | ❌ | ❌ |
| jsonschema-specifications | ✅ | ❌ | ❌ |
| referencing | ✅ | ❌ | ❌ |
| rpds-py | ✅ | ❌ | ❌ |
| mdurl | ✅ | ❌ | ❌ |

## 🎯 Deployment Strategy

### Step 1: Try Standard Requirements
```bash
# Use the main requirements file
cp requirements.txt requirements_deploy.txt
```

### Step 2: If Issues Occur
```bash
# Switch to minimal requirements
cp requirements_minimal.txt requirements_deploy.txt
```

### Step 3: If Still Having Issues
```bash
# Use ultra-conservative requirements
cp requirements_conservative.txt requirements_deploy.txt
```

### Step 4: Test Before Deploying
```bash
# Always test locally first
python deployment_test.py
```

## 📝 Notes

- **Standard requirements**: Best for most deployments
- **Minimal requirements**: Good fallback option
- **Conservative requirements**: Maximum compatibility
- **Always test locally** before deploying
- **Monitor deployment logs** for specific errors
- **Use Python 3.11** if Python 3.13 causes too many issues

## 🔄 Migration Path

1. **Start with conservative requirements**
2. **Test core functionality**
3. **Gradually add packages** from minimal requirements
4. **Finally add packages** from standard requirements
5. **Monitor for issues** at each step

---

**Remember**: It's better to start with fewer dependencies and add more as needed, rather than starting with too many and removing them when they cause issues. 