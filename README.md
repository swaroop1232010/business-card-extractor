# Business Card Extractor Pro

A professional AI-powered web application for extracting, storing, and managing business card information using OCR technology.

## 🚀 Features

- **AI-Powered OCR**: Advanced text extraction from business card images
- **Smart Database**: PostgreSQL/Supabase integration for data storage
- **Modern UI**: Responsive design with mobile-friendly interface
- **Export/Import**: CSV and Excel support for data management
- **Contact Management**: View, edit, and organize contact information
- **Cloud Deployment**: Ready for Streamlit Cloud deployment

## 📁 Project Structure

```
business-card-extractor/
├── main.py                 # Main application entry point
├── src/                    # Source code directory
│   ├── app.py             # Main Streamlit application
│   ├── core/              # Core functionality modules
│   │   ├── database.py    # Database operations
│   │   ├── preprocess.py  # Image preprocessing
│   │   ├── ocr.py         # OCR text extraction
│   │   └── classify.py    # Text classification
│   ├── utils/             # Utility modules
│   │   └── styles.py      # CSS styling
│   └── config/            # Configuration files
│       ├── config.py      # App configuration
│       ├── setup.sql      # Database schema
│       └── sample_contacts.csv
├── deployment/            # Deployment scripts and tools
│   ├── deploy.bat         # Windows deployment script
│   ├── deploy.sh          # Linux deployment script
│   ├── deployment_test.py # Deployment testing
│   ├── test_installation.py
│   ├── setup_venv.py
│   ├── setup.bat
│   └── run.bat
├── docs/                  # Documentation
│   ├── DEPLOYMENT.md
│   ├── DEPLOYMENT_TROUBLESHOOTING.md
│   ├── PYTHON_313_COMPATIBILITY.md
│   └── REQUIREMENTS_GUIDE.md
├── requirements.txt       # Main dependencies
├── requirements_minimal.txt
├── requirements_conservative.txt
├── packages.txt          # System dependencies
├── runtime.txt           # Python runtime
└── README.md            # This file
```

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd business-card-extractor
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   deployment\setup.bat
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # Windows
   deployment\run.bat
   
   # Linux/Mac
   streamlit run main.py
   ```

### Cloud Deployment

The application is configured to use Supabase defaults when deployed on Streamlit Cloud.

1. **Deploy to Streamlit Cloud**
   - Connect your GitHub repository
   - Set the main file path to `main.py`
   - Deploy automatically

2. **Environment Variables** (Optional)
   - `SUPABASE_HOST`: Your Supabase host
   - `SUPABASE_PORT`: Database port (default: 5432)
   - `SUPABASE_USER`: Database user (default: postgres)
   - `SUPABASE_PASSWORD`: Database password
   - `SUPABASE_DB`: Database name (default: postgres)

## 🗄️ Database Setup

The application uses PostgreSQL/Supabase for data storage. The database schema is automatically created on first run.

### Manual Setup (Optional)

```sql
-- Run setup.sql in your database
CREATE TABLE IF NOT EXISTS business_cards (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    designation VARCHAR(255),
    company VARCHAR(255),
    phone TEXT,
    email TEXT,
    website TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 Usage

1. **Extract Cards**: Upload business card images or use camera
2. **Manage Data**: Import/export contacts in CSV/Excel format
3. **View Contacts**: Browse and edit stored contact information
4. **Settings**: Configure application preferences

## 🔧 Configuration

The application uses centralized configuration in `src/config/config.py`:

- **Database Settings**: Supabase connection parameters
- **Upload Settings**: File type restrictions and size limits
- **OCR Settings**: Text extraction parameters
- **UI Settings**: Application appearance and behavior

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set main file to `main.py`
4. Deploy automatically

### Local Production

```bash
# Run deployment test
python deployment/deployment_test.py

# Deploy using scripts
# Windows
deployment\deploy.bat

# Linux
deployment/deploy.sh
```

## 📝 Requirements

### Python Dependencies
- `streamlit>=1.28.0`
- `opencv-python>=4.8.0`
- `pytesseract>=0.3.10`
- `psycopg2-binary>=2.9.0`
- `pandas>=2.0.0`
- `pillow>=10.0.0`

### System Dependencies
- Tesseract OCR
- OpenCV system libraries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For deployment issues, see:
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](docs/DEPLOYMENT_TROUBLESHOOTING.md)
- [Python 3.13 Compatibility](docs/PYTHON_313_COMPATIBILITY.md)
- [Requirements Guide](docs/REQUIREMENTS_GUIDE.md)

## 🔄 Version History

- **v2.0**: Professional project structure with Supabase integration
- **v1.0**: Initial release with basic OCR functionality 