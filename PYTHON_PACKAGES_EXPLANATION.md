# Why We Need `__init__.py` Files

## What are `__init__.py` files?

`__init__.py` files are special Python files that tell Python that a directory should be treated as a **package** (a collection of modules).

## Why do we need them?

### 1. **Package Recognition**
Without `__init__.py` files, Python doesn't recognize directories as packages, so you can't import modules from them.

### 2. **Import System**
Python's import system requires these files to:
- Find modules in subdirectories
- Resolve import paths correctly
- Handle relative imports

### 3. **Our Project Structure**
```
src/
├── __init__.py          # Makes src a package
├── core/
│   ├── __init__.py      # Makes core a package
│   ├── database.py
│   ├── ocr.py
│   └── classify.py
├── utils/
│   ├── __init__.py      # Makes utils a package
│   └── styles.py
└── config/
    ├── __init__.py      # Makes config a package
    └── config.py
```

## What happens without them?

**Error:** `KeyError: 'core'` or `ImportError: No module named 'core'`

This happens because Python can't find the modules when trying to import:
```python
from core.database import db_manager  # ❌ Fails without __init__.py
```

## What we added:

1. `src/core/__init__.py` - Makes `core` directory importable
2. `src/utils/__init__.py` - Makes `utils` directory importable  
3. `src/config/__init__.py` - Makes `config` directory importable

## Result:

Now these imports work correctly:
```python
from core.database import db_manager      # ✅ Works
from utils.styles import get_css_styles   # ✅ Works
from config.config import APP_CONFIG      # ✅ Works
```

## Note:
The `__init__.py` files can be empty (which is what we used) or contain package initialization code. Empty files are perfectly fine for basic package recognition. 