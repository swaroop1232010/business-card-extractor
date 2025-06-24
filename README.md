# Business Card Extraction System

A Python-based web application for extracting business card information from images using OCR and storing the data in a MySQL database.

## 🚀 Features

- **Image Upload**: Upload business card images (JPG/PNG)
- **Image Preprocessing**: Automatic image enhancement using OpenCV
- **OCR Processing**: Text extraction using EasyOCR
- **Smart Classification**: Automatic classification of extracted text into fields:
  - Name
  - Designation/Job Title
  - Company
  - Phone Numbers
  - Email Addresses
  - Websites
  - Address
- **Database Storage**: MySQL database integration
- **Web Interface**: Beautiful Streamlit web application
- **Search Functionality**: Search through stored contacts
- **Export/Import Data**: Export contacts to CSV/Excel and import from CSV
- **Error Handling**: Comprehensive error handling and user feedback

## 📁 Project Structure

```
business_card_extraction/
├── app.py              # Main Streamlit web application
├── preprocess.py       # Image preprocessing module
├── ocr.py             # OCR text extraction module
├── classify.py        # Text classification module
├── database.py        # Database operations module
├── requirements.txt   # Python dependencies
├── setup.sql         # MySQL database setup script
├── setup.bat         # Windows setup script (automated)
├── run.bat           # Windows run script (automated)
├── setup_venv.py     # Virtual environment setup script
├── test_installation.py # Installation verification script
├── sample_contacts.csv # Sample CSV file for import testing
├── temp/             # Temporary file storage
├── .gitignore        # Git ignore file
└── README.md         # This file
```

## 🛠️ Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **MySQL Server** (running locally or remotely)
3. **Git** (for cloning the repository)

### Method 1: Automated Setup (Windows) - RECOMMENDED

1. **Navigate to the project directory:**
   ```bash
   cd business_card_extraction
   ```

2. **Run the automated setup:**
   ```bash
   setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up everything automatically

3. **Run the application:**
   ```bash
   run.bat
   ```

### Method 2: Manual Setup

#### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd business_card_extraction
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Set Up MySQL Database

1. **Start MySQL Server** (if not already running)

2. **Create Database and Tables:**
   ```bash
   mysql -u your_username -p < setup.sql
   ```
   
   Or manually run the SQL commands in `setup.sql`:
   ```sql
   CREATE DATABASE IF NOT EXISTS business_cards;
   USE business_cards;
   
   CREATE TABLE IF NOT EXISTS contacts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       designation VARCHAR(100),
       company VARCHAR(100),
       phone VARCHAR(50),
       email VARCHAR(100),
       website VARCHAR(100),
       address VARCHAR(255),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

#### Step 5: Configure Database Connection

Update the database credentials in the application:

1. **Method 1**: Update in the web interface
   - Run the application
   - Use the sidebar to configure database settings
   - Test the connection

2. **Method 2**: Update in `database.py`
   ```python
   db_manager = DatabaseManager(
       host='localhost',
       user='your_username',
       password='your_password',
       database='business_cards'
   )
   ```

## 🚀 Running the Application

### Method 1: Using the Run Script (Windows)

```bash
run.bat
```

### Method 2: Manual Start

**Make sure your virtual environment is activated first:**

**Windows:**
```bash
venv\Scripts\activate
streamlit run app.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Database Configuration
- Use the sidebar to configure your MySQL database connection
- Click "Test Database Connection" to verify settings
- Ensure the connection is successful before proceeding

### 2. Upload Business Card
- Click "Browse files" to upload a business card image
- Supported formats: JPG, JPEG, PNG
- Ensure the image is clear and well-lit for best results

### 3. Extract Information
- Click "Extract Information" to process the image
- The app will:
  - Preprocess the image for better OCR
  - Extract text using EasyOCR
  - Classify the text into business card fields

### 4. Review and Save
- Review the extracted information
- Check both the formatted view and JSON format
- Click "Save to Database" if satisfied with the results

### 5. Export Data
- Go to the "Data Management" section
- Choose export format (CSV or Excel)
- Click "Export to [Format]" to download your contacts
- Use the template download for preparing import data

### 6. Import Data
- Download the CSV template to understand the required format
- Prepare your CSV file with contact information
- Upload the CSV file in the import section
- Choose whether to skip duplicates
- Click "Import Contacts" to add them to the database

### 7. View All Contacts
- Scroll down to see all stored contacts
- Use the search functionality to find specific contacts
- View contact details in a table format

## 📁 Data Management Features

### Export Functionality
- **CSV Export**: Export all contacts to CSV format
- **Excel Export**: Export all contacts to Excel format
- **Automatic Naming**: Files are automatically named with timestamps
- **Download Ready**: Files are immediately available for download

### Import Functionality
- **CSV Import**: Import contacts from CSV files
- **Template Download**: Download a CSV template with correct column structure
- **Duplicate Handling**: Option to skip or allow duplicate entries
- **Validation**: Automatic validation of CSV structure and data
- **Error Reporting**: Detailed error messages for failed imports

### CSV Template Structure
The CSV file should have the following columns:
```csv
name,designation,company,phone,email,website,address
John Doe,Software Engineer,Tech Corp,(555) 123-4567,john@techcorp.com,www.techcorp.com,123 Main St, City, State 12345
```

## 🔧 Configuration

### Database Settings
- **Host**: MySQL server address (default: localhost)
- **Username**: MySQL username
- **Password**: MySQL password
- **Database**: Database name (default: business_cards)

### OCR Settings
- **Language**: English (configurable in `ocr.py`)
- **GPU Support**: Set `gpu=True` in `ocr.py` if CUDA is available
- **Confidence Threshold**: Adjust in `ocr.py` (default: 0.5)

### Image Processing
- **Scale Factor**: Adjust in `preprocess.py` (default: 1.5x)
- **Threshold Method**: Adaptive thresholding for varying lighting
- **Noise Reduction**: Morphological operations and Gaussian blur

## 🔧 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'cv2'"**
   - **Solution**: Make sure you're in the virtual environment
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`
   - Then reinstall: `pip install -r requirements.txt`

2. **"File does not exist: app.py"**
   - **Solution**: Make sure you're in the `business_card_extraction` directory
   - Check your current directory: `dir` (Windows) or `ls` (Linux/Mac)

3. **Database Connection Failed**
   - Verify MySQL server is running
   - Check username and password
   - Ensure database exists
   - Check network connectivity

4. **OCR Not Working**
   - Ensure image is clear and well-lit
   - Check if image format is supported
   - Verify EasyOCR installation
   - Try different image preprocessing settings

5. **Virtual Environment Issues**
   - Delete the `venv` folder and recreate it
   - Run `setup.bat` again
   - Make sure Python 3.8+ is installed

6. **Import/Export Issues**
   - Check CSV file format matches the template
   - Ensure all required columns are present
   - Verify file encoding is UTF-8
   - Check file permissions

### Error Messages

- **"Image file not found"**: Check file path and permissions
- **"Unable to load image"**: Verify image format and corruption
- **"Database connection failed"**: Check MySQL settings and connectivity
- **"No text extracted"**: Try a different image or improve image quality
- **"Missing required columns"**: Use the provided CSV template
- **"Import failed"**: Check CSV format and data validity

## 📊 Performance Tips

1. **Image Quality**: Use high-resolution, well-lit images
2. **Text Clarity**: Ensure text is clearly visible and not blurry
3. **Background**: Use images with good contrast between text and background
4. **GPU Acceleration**: Enable GPU support for faster OCR processing
5. **Database Indexing**: The setup script includes indexes for better performance
6. **Batch Import**: Use CSV import for adding multiple contacts at once
7. **Regular Exports**: Export your data regularly as backup

## 🔒 Security Considerations

1. **Database Credentials**: Store credentials securely, not in code
2. **Input Validation**: All user inputs are validated
3. **File Upload**: Only image and CSV files are accepted
4. **SQL Injection**: Uses parameterized queries
5. **Temporary Files**: Automatically cleaned up after processing
6. **Data Privacy**: Export files are automatically deleted after download

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error logs
3. Create an issue in the repository
4. Contact the development team

## 🔄 Updates and Maintenance

- Regularly update dependencies
- Monitor database performance
- Backup database regularly
- Test with new business card formats
- Update classification patterns as needed
- Export data regularly for backup

---

**Happy Business Card Extraction! 📇✨** 