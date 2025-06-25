# Deployment Guide - Business Card Extractor Pro

## 🚀 Quick Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Professional project structure with Supabase integration"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set **Main file path** to: `main.py`
   - Click **Deploy**

3. **Environment Variables** (Optional)
   - `SUPABASE_HOST`: Your Supabase host
   - `SUPABASE_PORT`: Database port (default: 5432)
   - `SUPABASE_USER`: Database user (default: postgres)
   - `SUPABASE_PASSWORD`: Database password
   - `SUPABASE_DB`: Database name (default: postgres)

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

## 📁 Project Structure

```
business-card-extractor/
├── main.py                 # Entry point for Streamlit
├── src/                    # Source code
│   ├── app.py             # Main application
│   ├── core/              # Core modules
│   ├── utils/             # Utilities
│   └── config/            # Configuration
├── deployment/            # Deployment tools
├── docs/                  # Documentation
└── requirements.txt       # Dependencies
```

## 🔧 Configuration

The app automatically uses Supabase defaults when deployed:

- **Database**: PostgreSQL via Supabase
- **Host**: `db.ncjbnmsvthkttatdwdaz.supabase.co`
- **User**: `postgres`
- **Database**: `postgres`

## ✅ Verification

After deployment, verify:

1. **Database Connection**: Check if contacts can be saved
2. **OCR Functionality**: Test image upload and extraction
3. **Export/Import**: Test CSV/Excel operations
4. **Mobile Responsiveness**: Test on mobile devices

## 🆘 Troubleshooting

- **Import Errors**: Check `packages.txt` for system dependencies
- **Python Version**: Ensure Python 3.13 compatibility
- **OpenCV Issues**: Verify system libraries are installed
- **Database Errors**: Check Supabase connection settings

For detailed troubleshooting, see `docs/DEPLOYMENT_TROUBLESHOOTING.md` 