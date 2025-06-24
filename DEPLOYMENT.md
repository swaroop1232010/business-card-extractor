# Streamlit Cloud Deployment Guide

## Files Created/Modified for Deployment

### 1. `requirements.txt`
- Updated numpy to `>=1.26.0,<2.0.0` for pandas compatibility
- Changed `psycopg2-binary` to `psycopg2` for better compatibility
- Updated Pillow to `>=10.2.0` for Python 3.13 compatibility
- Updated openpyxl to `>=3.1.2` for better compatibility
- All other dependencies remain the same

### 2. `packages.txt` (NEW)
- Added PostgreSQL development libraries:
  - `libpq-dev` - Required for psycopg2 compilation
  - `postgresql-client` - PostgreSQL client utilities
- Added image processing libraries:
  - `libjpeg-dev`, `libpng-dev`, `libfreetype6-dev` - For Pillow
  - `liblcms2-dev`, `libopenjp2-7-dev`, `libtiff5-dev` - For additional image formats
  - `libwebp-dev`, `libharfbuzz-dev`, `libfribidi-dev` - For webp and text rendering
  - `libxcb1-dev` - For X11 support

### 3. `runtime.txt` (NEW)
- Specified Python 3.11.9 for better package compatibility
- Avoids Python 3.13 which has limited wheel support

### 4. `.streamlit/config.toml` (NEW)
- Optimized Streamlit configuration for cloud deployment
- Increased upload size limit
- Disabled unnecessary features for better performance

### 5. `pyproject.toml` (NEW)
- Modern Python packaging configuration
- Specifies Python >=3.11 requirement
- Helps with build system configuration

## Deployment Steps

1. **Push all changes to your GitHub repository**
2. **Connect to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set the main file path to: `app.py`
   - Click "Deploy"

3. **Environment Variables (if using external database):**
   - Add your database credentials in Streamlit Cloud settings
   - Example for PostgreSQL:
     ```
     DB_TYPE=postgresql
     DB_HOST=your-host.com
     DB_USER=your-username
     DB_PASSWORD=your-password
     DB_NAME=your-database
     DB_PORT=5432
     ```

## Troubleshooting

### If you get Pillow build errors:
1. **Check Python version:** Ensure `runtime.txt` specifies Python 3.11.9
2. **Verify packages.txt:** Make sure all image processing libraries are included
3. **Wait for build:** First deployment may take 5-10 minutes
4. **Alternative:** If still failing, try updating to Pillow 11.x in requirements.txt

### If you still get psycopg2 build errors:
1. **Check Python version:** Ensure `runtime.txt` specifies Python 3.11.9
2. **Verify packages.txt:** Make sure `libpq-dev` is included
3. **Wait for build:** First deployment may take 5-10 minutes

### If database connection fails:
1. **Check credentials:** Verify all environment variables
2. **Test connection:** Use the database test feature in the app
3. **Check firewall:** Ensure your database allows connections from Streamlit Cloud

### If Streamlit Cloud ignores runtime.txt:
1. **Contact Streamlit Support:** Some platforms may not respect runtime.txt
2. **Use environment variables:** Set Python version in Streamlit Cloud settings
3. **Consider alternative deployment:** Heroku, Railway, or other platforms

## Default Configuration

The app will default to SQLite if no database credentials are provided, which works immediately without any external database setup.

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify all files are committed to your repository
3. Ensure your database is accessible from external connections
4. Consider downgrading to Python 3.11 if Python 3.13 continues to cause issues 