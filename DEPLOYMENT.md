# Streamlit Cloud Deployment Guide

## Files Created/Modified for Deployment

### 1. `requirements.txt`
- Updated numpy to `>=1.26.0,<2.0.0` for pandas compatibility
- Changed `psycopg2-binary` to `psycopg2` for better compatibility
- All other dependencies remain the same

### 2. `packages.txt` (NEW)
- Added PostgreSQL development libraries:
  - `libpq-dev` - Required for psycopg2 compilation
  - `postgresql-client` - PostgreSQL client utilities

### 3. `runtime.txt` (NEW)
- Specified Python 3.11 for better package compatibility
- Avoids Python 3.13 which has limited wheel support

### 4. `.streamlit/config.toml` (NEW)
- Optimized Streamlit configuration for cloud deployment
- Increased upload size limit
- Disabled unnecessary features for better performance

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

### If you still get psycopg2 build errors:
1. **Check Python version:** Ensure `runtime.txt` specifies Python 3.11
2. **Verify packages.txt:** Make sure `libpq-dev` is included
3. **Wait for build:** First deployment may take 5-10 minutes

### If database connection fails:
1. **Check credentials:** Verify all environment variables
2. **Test connection:** Use the database test feature in the app
3. **Check firewall:** Ensure your database allows connections from Streamlit Cloud

## Default Configuration

The app will default to SQLite if no database credentials are provided, which works immediately without any external database setup.

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify all files are committed to your repository
3. Ensure your database is accessible from external connections 