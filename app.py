"""
Business Card Extraction Web Application - Enhanced UI
Streamlit app for extracting business card information from images and storing in MySQL database.
"""

import streamlit as st
import os
import tempfile
import json
from pathlib import Path
import logging
import pandas as pd

# Import custom modules
from preprocess import preprocess_image
from ocr import extract_text
from classify import classify_text
from database import (
    store_in_db, get_all_contacts, db_manager, set_db_config, 
    export_to_csv, export_to_excel, import_from_csv, get_export_template,
    update_contact
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration with production optimizations
st.set_page_config(
    page_title="Business Card Extractor Pro",
    page_icon="📇",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/business-card-extractor',
        'Report a bug': 'https://github.com/your-repo/business-card-extractor/issues',
        'About': 'Business Card Extractor Pro - AI-powered OCR for business cards'
    }
)

# Enhanced CSS for modern, user-friendly design with mobile responsiveness
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: clamp(2rem, 5vw, 3rem);
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: clamp(1rem, 3vw, 1.5rem);
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    
    .success-card {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        color: #155724;
    }
    
    .error-card {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    
    .info-card {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 4px solid #17a2b8;
        color: #0c5460;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s ease;
        min-height: 44px; /* Mobile-friendly touch target */
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Progress indicators */
    .progress-step {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #e9ecef;
        text-align: center;
        line-height: 30px;
        margin-right: 10px;
        font-weight: bold;
    }
    
    .progress-step.active {
        background: #1f77b4;
        color: white;
    }
    
    .progress-step.completed {
        background: #28a745;
        color: white;
    }
    
    /* Data display styling */
    .data-field {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        border-left: 3px solid #1f77b4;
    }
    
    .data-label {
        font-weight: 600;
        color: #495057;
        margin-bottom: 0.25rem;
    }
    
    .data-value {
        color: #212529;
        font-size: 1.1rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: clamp(1.5rem, 4vw, 1.8rem);
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1f77b4;
        font-weight: 600;
    }
    
    /* Feature highlights */
    .feature-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1rem;
        }
        
        .section-header {
            font-size: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.75rem 1.5rem;
            font-size: 0.9rem;
        }
        
        .feature-highlight {
            padding: 0.75rem;
            font-size: 0.9rem;
        }
        
        /* Improve table responsiveness */
        .stDataFrame {
            font-size: 0.8rem;
        }
        
        /* Better spacing for mobile */
        .stMarkdown {
            margin-bottom: 1rem;
        }
        
        /* Hide unnecessary elements on mobile */
        .mobile-hide {
            display: none !important;
        }
        
        /* Compact layout for mobile */
        .mobile-compact {
            padding: 0.5rem !important;
            margin: 0.25rem 0 !important;
        }
        
        /* Optimize sidebar for mobile */
        .css-1d391kg {
            padding: 0.5rem !important;
        }
        
        /* Better mobile navigation */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* Camera input styling */
    .stCameraInput {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    
    /* Status indicators */
    .stStatus {
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Mobile-specific optimizations */
    @media (max-width: 480px) {
        /* Even more compact for small screens */
        .main-header {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        
        .sub-header {
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        /* Reduce padding and margins */
        .stMarkdown {
            margin-bottom: 0.5rem;
        }
        
        /* Compact buttons */
        .stButton > button {
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            min-height: 40px;
        }
        
        /* Hide feature highlights on very small screens */
        .feature-highlight {
            display: none;
        }
    }
    
    /* Contact action buttons styling */
    .contact-action-btn {
        margin: 0.25rem;
        border-radius: 8px;
        font-size: 0.9rem;
        min-height: 36px;
    }
    
    /* Form styling */
    .stForm {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background: #e9ecef;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Contact details display */
    .contact-details {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    /* Export buttons */
    .export-btn {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .export-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Popup dialog styling */
    .popup-dialog {
        background: white;
        border: 2px solid #1f77b4;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Action button styling */
    .action-btn {
        margin: 0.25rem;
        border-radius: 6px;
        font-size: 0.85rem;
        min-height: 32px;
        transition: all 0.2s ease;
    }
    
    .action-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Contact row styling */
    .contact-row {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #1f77b4;
    }
    
    /* Performance optimizations */
    .stButton > button {
        transition: all 0.15s ease; /* Faster transitions */
    }
    
    .stDataFrame {
        font-size: 0.9rem; /* Slightly smaller for better performance */
    }
    
    /* Compact action buttons */
    .compact-action-btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        min-height: 28px;
        border-radius: 4px;
    }
    
    /* Optimized loading states */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #f3f3f3;
        border-top: 2px solid #1f77b4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# --- Place these at the top, after imports ---
SUPABASE_DEFAULTS = {
    "host": os.environ.get("SUPABASE_HOST", "db.ncjbnmsvthkttatdwdaz.supabase.co"),
    "port": os.environ.get("SUPABASE_PORT", "5432"),
    "user": os.environ.get("SUPABASE_USER", "postgres"),
    "password": os.environ.get("SUPABASE_PASSWORD", "fmv_v7UjDN+&Td&"),
    "database": os.environ.get("SUPABASE_DB", "postgres")
}

def get_supabase_db_config():
    return (
        "postgresql",
        SUPABASE_DEFAULTS["host"],
        SUPABASE_DEFAULTS["user"],
        SUPABASE_DEFAULTS["password"],
        SUPABASE_DEFAULTS["database"],
        SUPABASE_DEFAULTS["port"],
        None
    )

# Set the DB config at app startup
set_db_config(*get_supabase_db_config())

# Initialize session state for better performance
def init_session_state():
    """Initialize session state variables."""
    if 'extracting' not in st.session_state:
        st.session_state['extracting'] = False
    if 'extraction_done' not in st.session_state:
        st.session_state['extraction_done'] = False
    if 'delete_confirm_id' not in st.session_state:
        st.session_state['delete_confirm_id'] = None
    if 'delete_confirm_name' not in st.session_state:
        st.session_state['delete_confirm_name'] = None

# Production-ready error handling
def handle_global_exceptions(func):
    """Decorator to handle global exceptions gracefully."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            logger.error(f"Global error in {func.__name__}: {e}")
            return None
    return wrapper

# Resource cleanup
def cleanup_temp_files():
    """Clean up temporary files for better performance."""
    try:
        temp_dir = Path("temp")
        if temp_dir.exists():
            for file in temp_dir.glob("*"):
                try:
                    file.unlink()
                except:
                    pass
    except Exception as e:
        logger.warning(f"Error cleaning temp files: {e}")

def main():
    """Main application function."""
    
    # Initialize session state
    init_session_state()
    
    # Clean up temporary files on startup
    cleanup_temp_files()
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-header">📇 Business Card Extractor Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Extract, Store, and Manage Business Card Information with AI-Powered OCR</p>', unsafe_allow_html=True)
    
    # Feature highlights (hidden on mobile)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-highlight">🔍 AI-Powered OCR</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-highlight">💾 Smart Database</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-highlight">📊 Export/Import</div>', unsafe_allow_html=True)
    
    # Main content area with tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Extract Cards", "📊 Manage Data", "📋 View Contacts", "⚙️ Settings"])
    
    with tab1:
        extract_business_cards()
    
    with tab2:
        manage_data()
    
    with tab3:
        view_contacts()
    
    with tab4:
        show_settings()


def extract_business_cards():
    """Tab for business card extraction."""
    
    st.markdown('<h2 class="section-header">📤 Extract Business Card Information</h2>', unsafe_allow_html=True)
    
    # Mobile-friendly progress display
    if st.checkbox("📱 Show Progress Steps", value=True, help="Show/hide the progress steps"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="progress-step active">1</div>', unsafe_allow_html=True)
            st.markdown("**Upload**")
        with col2:
            st.markdown('<div class="progress-step">2</div>', unsafe_allow_html=True)
            st.markdown("**Process**")
        with col3:
            st.markdown('<div class="progress-step">3</div>', unsafe_allow_html=True)
            st.markdown("**Extract**")
        with col4:
            st.markdown('<div class="progress-step">4</div>', unsafe_allow_html=True)
            st.markdown("**Save**")
    
    # --- Professional Upload Section ---
    st.markdown('''
    <div class="card" style="margin-bottom:2rem;">
        <h3 style="margin-bottom:0.5rem;">📤 <span style="vertical-align:middle;">Upload Business Card</span></h3>
        <div style="display:flex;flex-wrap:wrap;gap:2rem;align-items:center;">
            <div style="flex:1;min-width:220px;">
                <b>📷 Take Photo</b><br>
                <span style="font-size:0.95em;color:#555;">Use your device camera to capture a business card.</span>
            </div>
            <div style="flex:1;min-width:220px;">
                <b>📁 Upload Image(s)</b><br>
                <span style="font-size:0.95em;color:#555;">Select one or more images from your device.</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Camera toggle
    use_camera = st.checkbox("📷 Use Camera", help="Check this to take a photo with your device camera")
    camera_photo = None
    if use_camera:
        camera_photo = st.camera_input(
            "Take a photo of the business card",
            help="Click the camera button to take a photo. Works on mobile devices and web browsers with camera access.",
            key="camera_input"
        )
        if camera_photo:
            st.success("✅ Photo captured successfully!")

    uploaded_files = st.file_uploader(
        "Upload image(s) of business cards (JPG, PNG)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        disabled=st.session_state.get('extracting', False)
    )

    # Combine camera photo and uploaded files
    all_files = []
    if camera_photo:
        all_files.append(("Camera", camera_photo))
    if uploaded_files:
        for file in uploaded_files:
            all_files.append(("Upload", file))

    # Show previews
    if all_files:
        for idx, (source, file) in enumerate(all_files):
            st.markdown(f"#### {source} - Card {idx+1}")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(file, caption=f"{source} - Card {idx+1}", use_column_width=True)
            with col2:
                st.markdown(f"**Image Preview:**\n- ✅ File uploaded successfully\n- 📏 Size: {file.size/1024:.1f} KB\n- 📄 Format: {file.type}")

    # Extraction logic
    if all_files:
        if not st.session_state.get('extracting', False):
            if st.button("🚀 Extract Information for All Cards", key="extract_all", disabled=st.session_state.get('extracting', False)):
                st.session_state['extracting'] = True
                st.experimental_rerun()

        # Extraction process
        if st.session_state.get('extracting', False) and not st.session_state.get('extraction_done', False):
            with st.spinner("🔄 Extracting information from all cards..."):
                extraction_results = []
                temp_files = []  # Track temp files for cleanup
                
                try:
                    for idx, (source, uploaded_file) in enumerate(all_files):
                        st.markdown(f"### 📄 Processing {source} - Card {idx+1}/{len(all_files)}")
                        
                        # Step 1: Preprocess image
                        with st.status(f"📸 Preprocessing {source} - Card {idx+1}...", expanded=True) as status:
                            try:
                                temp_dir = Path("temp")
                                temp_dir.mkdir(exist_ok=True)
                                
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir=temp_dir) as tmp_file:
                                    tmp_file.write(uploaded_file.getvalue())
                                    temp_image_path = tmp_file.name
                                    temp_files.append(temp_image_path)
                                
                                processed_image, processed_path = preprocess_image(temp_image_path)
                                temp_files.append(processed_path)
                                status.update(label=f"✅ Preprocessing completed for {source} - Card {idx+1}", state="complete")
                                st.success("✅ Image preprocessing completed")
                            except Exception as e:
                                status.update(label=f"❌ Preprocessing failed for {source} - Card {idx+1}", state="error")
                                st.error(f"❌ Image preprocessing failed: {str(e)}")
                                st.session_state[f'extracted_data_{idx}'] = {
                                    'raw_text': '',
                                    'classified_data': {'error': f'Preprocessing failed: {str(e)}'}
                                }
                                extraction_results.append(False)
                                continue
                        
                        # Step 2: Extract text using OCR
                        with st.status(f"🔤 Extracting text from {source} - Card {idx+1}...", expanded=True) as status:
                            try:
                                extracted_text = extract_text(processed_path)
                                if not extracted_text.strip():
                                    status.update(label=f"⚠️ No text extracted from {source} - Card {idx+1}", state="error")
                                    st.warning(f"⚠️ No text could be extracted from {source} - Card {idx+1}")
                                    st.session_state[f'extracted_data_{idx}'] = {
                                        'raw_text': '',
                                        'classified_data': {'error': 'No text could be extracted'}
                                    }
                                    extraction_results.append(False)
                                    continue
                                status.update(label=f"✅ Text extraction completed for {source} - Card {idx+1}", state="complete")
                                st.success("✅ Text extraction completed")
                            except Exception as e:
                                status.update(label=f"❌ Text extraction failed for {source} - Card {idx+1}", state="error")
                                st.error(f"❌ Text extraction failed: {str(e)}")
                                st.session_state[f'extracted_data_{idx}'] = {
                                    'raw_text': '',
                                    'classified_data': {'error': f'Text extraction failed: {str(e)}'}
                                }
                                extraction_results.append(False)
                                continue
                        
                        # Step 3: Classify extracted text
                        with st.status(f"🏷️ Classifying information from {source} - Card {idx+1}...", expanded=True) as status:
                            try:
                                classified_data = classify_text(extracted_text)
                                status.update(label=f"✅ Classification completed for {source} - Card {idx+1}", state="complete")
                                st.success("✅ Information classification completed")
                                
                                st.session_state[f'extracted_data_{idx}'] = {
                                    'raw_text': extracted_text,
                                    'classified_data': classified_data
                                }
                                extraction_results.append(True)
                                
                            except Exception as e:
                                status.update(label=f"❌ Classification failed for {source} - Card {idx+1}", state="error")
                                st.error(f"❌ Information classification failed: {str(e)}")
                                st.session_state[f'extracted_data_{idx}'] = {
                                    'raw_text': extracted_text,
                                    'classified_data': {'error': f'Classification failed: {str(e)}'}
                                }
                                extraction_results.append(False)
                                logger.error(f"Error classifying {source} - card {idx+1}: {e}")
                        
                        st.markdown("---")
                    
                    # Show final summary
                    success_count = sum(extraction_results)
                    total_count = len(extraction_results)
                    
                    if success_count > 0:
                        st.success(f"🎉 **Extraction Summary**: Successfully processed {success_count} out of {total_count} cards")
                    else:
                        st.error("❌ **Extraction Summary**: Failed to process any cards")
                        
                finally:
                    # Clean up temp files
                    for temp_file in temp_files:
                        try:
                            if os.path.exists(temp_file):
                                os.unlink(temp_file)
                        except:
                            pass
                
                st.session_state['extraction_done'] = True
                st.session_state['extracting'] = False
                st.experimental_rerun()

        # Show extracted data and save buttons
        if st.session_state.get('extraction_done', False):
            for idx, (source, uploaded_file) in enumerate(all_files):
                st.markdown(f"### 📊 Extracted Information for {source} - Card {idx+1}")
                data = st.session_state.get(f'extracted_data_{idx}', None)
                if data:
                    display_extracted_data_enhanced(data)
                    if st.button(f"💾 Save to Database ({source} - Card {idx+1})", key=f"save_{idx}", disabled=st.session_state.get('extracting', False)):
                        save_to_database(data)

            # Reset extraction state if user uploads new files
            if st.button("🔄 Extract New Cards", key="reset_extraction", disabled=st.session_state.get('extracting', False)):
                for idx in range(len(all_files)):
                    st.session_state.pop(f'extracted_data_{idx}', None)
                st.session_state['extraction_done'] = False
                st.session_state['extracting'] = False
                st.experimental_rerun()

    # Disable all other UI actions while extracting
    if st.session_state.get('extracting', False):
        st.info("⏳ Extraction in progress. Please wait until all cards are processed. Other actions are temporarily disabled.")
        st.stop()


def manage_data():
    """Tab for data management (export/import)."""
    
    st.markdown('<h2 class="section-header">📊 Data Management</h2>', unsafe_allow_html=True)
    
    col_export, col_import = st.columns(2)
    
    with col_export:
        st.markdown("### 📤 Export Data")
        st.markdown("Export your contacts to various formats:")
        
        # Export options
        export_format = st.selectbox(
            "Choose Export Format",
            ["CSV", "Excel"],
            help="CSV for spreadsheet applications, Excel for advanced formatting"
        )
        
        if st.button(f"📥 Export to {export_format}", type="secondary", use_container_width=True):
            export_data(export_format)
        
        st.markdown("---")
        st.markdown("### 📋 Download Template")
        st.markdown("Get a CSV template to prepare your data for import:")
        
        template_csv = get_export_template()
        st.download_button(
            label="📄 Download CSV Template",
            data=template_csv,
            file_name="contacts_template.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download a template CSV file with the correct column structure"
        )
    
    with col_import:
        st.markdown("### 📥 Import Data")
        st.markdown("Import contacts from a CSV file:")
        
        # File uploader for CSV import
        uploaded_csv = st.file_uploader(
            "Choose a CSV file to import",
            type=['csv'],
            help="Upload a CSV file with contact information in the correct format"
        )
        
        if uploaded_csv is not None:
            # Show CSV preview
            try:
                import pandas as pd
                df_preview = pd.read_csv(uploaded_csv)
                
                st.markdown("**📋 CSV Preview:**")
                st.dataframe(df_preview.head(), use_container_width=True)
                
                st.markdown(f"**📊 File Info:**")
                st.markdown(f"- Rows: {len(df_preview)}")
                st.markdown(f"- Columns: {', '.join(df_preview.columns)}")
                
                # Import options
                skip_duplicates = st.checkbox(
                    "Skip duplicates", 
                    value=True, 
                    help="Skip contacts that already exist in the database"
                )
                
                if st.button("📥 Import Contacts", type="secondary", use_container_width=True):
                    import_data(uploaded_csv, skip_duplicates)
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")


@st.cache_data(ttl=60)  # Cache for 1 minute - faster refresh
def get_cached_contacts():
    """Get all contacts with optimized caching."""
    return get_all_contacts()

def view_contacts():
    """Tab for viewing, editing, and managing contacts with optimized performance."""
    
    st.markdown('<h2 class="section-header">📋 Contact Management</h2>', unsafe_allow_html=True)
    
    # Show all contacts
    st.markdown("### 📊 All Contacts")
    
    try:
        # Get all contacts with optimized caching
        with st.spinner("📊 Loading contacts..."):
            contacts_df = get_cached_contacts()
        
        if contacts_df is None:
            st.error("❌ Failed to retrieve contacts from database")
            return
        
        if len(contacts_df) == 0:
            st.info("📭 No contacts found in database")
            return
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Contacts", len(contacts_df))
        with col2:
            st.metric("Companies", contacts_df['company'].nunique())
        with col3:
            st.metric("With Email", len(contacts_df[contacts_df['email'].notna() & (contacts_df['email'] != '')]))
        with col4:
            st.metric("With Phone", len(contacts_df[contacts_df['phone'].notna() & (contacts_df['phone'] != '')]))
        
        # Export functionality
        st.markdown("### 📤 Export Options")
        export_col1, export_col2, export_col3, export_col4 = st.columns(4)
        
        with export_col1:
            if st.button("📄 Export to CSV", type="secondary", use_container_width=True):
                export_data("CSV")
                
        with export_col2:
            if st.button("📊 Export to Excel", type="secondary", use_container_width=True):
                export_data("Excel")
                
        with export_col3:
            if st.button("🔄 Refresh Data", type="secondary", use_container_width=True):
                clear_contact_cache()
                st.experimental_rerun()
        
        with export_col4:
            if st.button("🔍 Check Duplicates", type="secondary", use_container_width=True):
                check_existing_duplicates(contacts_df)
        
        # Display contacts in a table with actions
        show_contacts_table_with_actions(contacts_df)
        
    except Exception as e:
        error_msg = str(e)
        show_database_error_message(error_msg)
        logger.error(f"Error displaying contacts: {e}")


def show_contacts_table_with_actions(df):
    """Display contacts in a modern, interactive table with enhanced features."""
    st.markdown("### 📊 Contact Data Table")
    
    # Add table controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Sort options
        sort_by = st.selectbox(
            "📊 Sort by",
            ["Created Date (Newest)", "Created Date (Oldest)", "Name (A-Z)", "Name (Z-A)", "Company (A-Z)", "Company (Z-A)"],
            help="Sort the contacts table"
        )
    
    with col2:
        # Name filter
        name_filter = st.text_input(
            "🔍 Filter by name",
            placeholder="Enter name to filter...",
            help="Filter contacts by name (case-insensitive)"
        )
    
    with col3:
        # Items per page
        items_per_page = st.selectbox(
            "📄 Items per page",
            [10, 25, 50, 100],
            index=1,
            help="Number of contacts to display per page"
        )
    
    # Process the dataframe for display
    display_df = df.copy()
    
    # Apply name filter
    if name_filter and name_filter.strip():
        try:
            name_mask = display_df['name'].str.contains(name_filter, case=False, na=False)
            display_df = display_df[name_mask]
            st.success(f"🔍 Found {len(display_df)} contacts matching '{name_filter}'")
        except Exception as e:
            st.error(f"❌ Error applying name filter: {str(e)}")
            display_df = df.copy()
    
    # Apply sorting
    if sort_by == "Created Date (Newest)":
        display_df = display_df.sort_values('created_at', ascending=False)
    elif sort_by == "Created Date (Oldest)":
        display_df = display_df.sort_values('created_at', ascending=True)
    elif sort_by == "Name (A-Z)":
        display_df = display_df.sort_values('name', ascending=True)
    elif sort_by == "Name (Z-A)":
        display_df = display_df.sort_values('name', ascending=False)
    elif sort_by == "Company (A-Z)":
        display_df = display_df.sort_values('company', ascending=True)
    elif sort_by == "Company (Z-A)":
        display_df = display_df.sort_values('company', ascending=False)
    
    # Pagination
    total_rows = len(display_df)
    total_pages = (total_rows + items_per_page - 1) // items_per_page
    
    if total_pages > 1:
        current_page = st.selectbox(
            f"📄 Page (1-{total_pages})",
            range(1, total_pages + 1),
            index=0,
            help=f"Showing {items_per_page} contacts per page"
        )
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_rows)
        display_df = display_df.iloc[start_idx:end_idx]
    
    # Prepare dataframe for display with action buttons
    if len(display_df) > 0:
        # Create a copy for display with formatted columns
        table_df = display_df.copy()
        
        # Format columns for better display
        table_df['ID'] = table_df['id'].astype(str)
        table_df['Name'] = table_df['name'].fillna('N/A')
        table_df['Designation'] = table_df['designation'].fillna('N/A')
        table_df['Company'] = table_df['company'].fillna('N/A')
        table_df['Phone'] = table_df['phone'].fillna('N/A')
        table_df['Email'] = table_df['email'].fillna('N/A')
        table_df['Website'] = table_df['website'].fillna('N/A')
        table_df['Address'] = table_df['address'].fillna('N/A')
        table_df['Created'] = pd.to_datetime(table_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Select columns for display
        display_columns = ['ID', 'Name', 'Designation', 'Company', 'Phone', 'Email', 'Website', 'Address', 'Created']
        table_df = table_df[display_columns]
        
        # Display the table with enhanced styling
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    help="Contact ID",
                    width="small"
                ),
                "Name": st.column_config.TextColumn(
                    "Name",
                    help="Contact name",
                    width="medium"
                ),
                "Designation": st.column_config.TextColumn(
                    "Designation",
                    help="Job title or designation",
                    width="medium"
                ),
                "Company": st.column_config.TextColumn(
                    "Company",
                    help="Company name",
                    width="medium"
                ),
                "Phone": st.column_config.TextColumn(
                    "Phone",
                    help="Phone number(s)",
                    width="medium"
                ),
                "Email": st.column_config.TextColumn(
                    "Email",
                    help="Email address(es)",
                    width="medium"
                ),
                "Website": st.column_config.TextColumn(
                    "Website",
                    help="Website URL(s)",
                    width="medium"
                ),
                "Address": st.column_config.TextColumn(
                    "Address",
                    help="Contact address",
                    width="large"
                ),
                "Created": st.column_config.DatetimeColumn(
                    "Created",
                    help="Date and time created",
                    width="medium",
                    format="DD-MM-YYYY HH:mm"
                )
            }
        )
        
        # Display summary
        st.markdown(f"**📊 Showing {len(display_df)} of {total_rows} contacts**")
        
        # Action buttons for selected contact
        st.markdown("### 🎯 Contact Actions")
        st.markdown("Select a contact ID to perform actions:")
        
        # Get unique IDs for selection
        contact_ids = display_df['id'].tolist()
        selected_id = st.selectbox(
            "Choose Contact ID",
            contact_ids,
            format_func=lambda x: f"ID {x} - {display_df[display_df['id'] == x]['name'].iloc[0]}",
            help="Select a contact to view, edit, or delete"
        )
        
        if selected_id:
            selected_contact = display_df[display_df['id'] == selected_id].iloc[0]
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("👁️ View Details", key=f"view_{selected_id}", use_container_width=True):
                    st.session_state['popup_action'] = 'view'
                    st.session_state['popup_contact_id'] = selected_id
                    st.experimental_rerun()
            
            with col2:
                if st.button("✏️ Edit Contact", key=f"edit_{selected_id}", use_container_width=True):
                    st.session_state['popup_action'] = 'edit'
                    st.session_state['popup_contact_id'] = selected_id
                    st.experimental_rerun()
            
            with col3:
                if st.button("🗑️ Delete Contact", key=f"delete_{selected_id}", use_container_width=True):
                    st.session_state['popup_action'] = 'delete'
                    st.session_state['popup_contact_id'] = selected_id
                    st.experimental_rerun()
            
            with col4:
                if st.button("📋 Copy Details", key=f"copy_{selected_id}", use_container_width=True):
                    # Create a formatted string for copying
                    contact_text = f"""
Name: {selected_contact.get('name', 'N/A')}
Designation: {selected_contact.get('designation', 'N/A')}
Company: {selected_contact.get('company', 'N/A')}
Phone: {selected_contact.get('phone', 'N/A')}
Email: {selected_contact.get('email', 'N/A')}
Website: {selected_contact.get('website', 'N/A')}
Address: {selected_contact.get('address', 'N/A')}
                    """.strip()
                    
                    st.code(contact_text, language=None)
                    st.success("✅ Contact details copied to clipboard (select and copy the text above)")
        
        # Handle popup dialogs
        if st.session_state.get('popup_action') and st.session_state.get('popup_contact_id'):
            action = st.session_state['popup_action']
            contact_id = st.session_state['popup_contact_id']
            contact_data = df[df['id'] == contact_id].iloc[0] if len(df[df['id'] == contact_id]) > 0 else None
            if contact_data is not None:
                with st.container():
                    st.markdown("---")
                    st.markdown('<div class="popup-dialog">', unsafe_allow_html=True)
                    st.markdown("### 🪟 Action Dialog")
                    if action == 'view':
                        st.markdown("#### 👁️ View Contact Details")
                        display_contact_details(contact_data)
                    elif action == 'edit':
                        st.markdown("#### ✏️ Edit Contact")
                        edit_contact_form(contact_id, contact_data)
                    elif action == 'delete':
                        st.markdown("#### 🗑️ Delete Contact")
                        st.warning(f"⚠️ Are you sure you want to delete **{contact_data.get('name', 'Unknown')}**?")
                        confirm_col, cancel_col = st.columns(2)
                        with confirm_col:
                            if st.button("✅ Confirm Delete", key=f"confirm_delete_{contact_id}", type="primary"):
                                try:
                                    success = db_manager.delete_contact(contact_id)
                                    if success:
                                        st.success(f"✅ Deleted contact: {contact_data.get('name', 'Unknown')}")
                                        clear_contact_cache()
                                        st.session_state['popup_action'] = None
                                        st.session_state['popup_contact_id'] = None
                                        st.session_state["action_row"] = None
                                        st.session_state["action_type"] = None
                                        st.experimental_rerun()
                                    else:
                                        st.error("❌ Failed to delete contact")
                                except Exception as e:
                                    error_msg = str(e)
                                    show_database_error_message(error_msg)
                        with cancel_col:
                            if st.button("❌ Cancel", key=f"cancel_delete_{contact_id}"):
                                st.session_state['popup_action'] = None
                                st.session_state['popup_contact_id'] = None
                                st.session_state["action_row"] = None
                                st.session_state["action_type"] = None
                                st.experimental_rerun()
                    if st.button("❌ Close Dialog", key=f"close_dialog_{contact_id}"):
                        st.session_state['popup_action'] = None
                        st.session_state['popup_contact_id'] = None
                        st.session_state["action_row"] = None
                        st.session_state["action_type"] = None
                        st.experimental_rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("📭 No contacts found matching your criteria")


def display_contact_details(contact_row):
    """Display detailed contact information."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **👤 Personal Information**
        - **Name:** {contact_row.get('name', 'N/A')}
        - **Designation:** {contact_row.get('designation', 'N/A')}
        - **Company:** {contact_row.get('company', 'N/A')}
        """)
        
        st.markdown(f"""
        **📞 Contact Information**
        - **Phone:** {contact_row.get('phone', 'N/A')}
        - **Email:** {contact_row.get('email', 'N/A')}
        - **Website:** {contact_row.get('website', 'N/A')}
        """)
    
    with col2:
        st.markdown(f"""
        **📍 Address**
        {contact_row.get('address', 'N/A')}
        """)
        
        st.markdown(f"""
        **📅 Created:** {contact_row.get('created_at', 'N/A')}
        **🆔 ID:** {contact_row.get('id', 'N/A')}
        """)


def edit_contact_form(contact_id, contact_data):
    """Form for editing contact information."""
    
    # Convert comma-separated strings to lists for editing
    phone_list = contact_data.get('phone', '').split(', ') if contact_data.get('phone') else []
    email_list = contact_data.get('email', '').split(', ') if contact_data.get('email') else []
    website_list = contact_data.get('website', '').split(', ') if contact_data.get('website') else []
    
    with st.form(key=f"edit_form_{contact_id}"):
        st.markdown("#### Edit Contact Information")
        
        # Personal Information
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", value=contact_data.get('name', ''), key=f"name_{contact_id}")
            designation = st.text_input("Designation", value=contact_data.get('designation', ''), key=f"designation_{contact_id}")
            company = st.text_input("Company", value=contact_data.get('company', ''), key=f"company_{contact_id}")
        
        with col2:
            # Phone numbers (multiple)
            phone_input = st.text_area("Phone Numbers (one per line)", 
                                      value='\n'.join(phone_list), 
                                      key=f"phone_{contact_id}",
                                      help="Enter multiple phone numbers, one per line")
            
            # Email addresses (multiple)
            email_input = st.text_area("Email Addresses (one per line)", 
                                      value='\n'.join(email_list), 
                                      key=f"email_{contact_id}",
                                      help="Enter multiple email addresses, one per line")
        
        # Website and Address
        website_input = st.text_area("Websites (one per line)", 
                                    value='\n'.join(website_list), 
                                    key=f"website_{contact_id}",
                                    help="Enter multiple websites, one per line")
        
        address = st.text_area("Address", value=contact_data.get('address', ''), key=f"address_{contact_id}")
        
        # Form buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            submit_button = st.form_submit_button("💾 Save Changes", type="primary")
        with col2:
            cancel_button = st.form_submit_button("❌ Cancel")
        with col3:
            reset_button = st.form_submit_button("🔄 Reset")
        
        if submit_button:
            # Process the form data
            phone_numbers = [p.strip() for p in phone_input.split('\n') if p.strip()]
            email_addresses = [e.strip() for e in email_input.split('\n') if e.strip()]
            websites = [w.strip() for w in website_input.split('\n') if w.strip()]
            
            # Prepare updated data
            updated_data = {
                'name': name,
                'designation': designation,
                'company': company,
                'phone': phone_numbers,
                'email': email_addresses,
                'website': websites,
                'address': address
            }
            
            # Update the contact
            try:
                success = update_contact(contact_id, updated_data)
                if success:
                    st.success(f"✅ Contact updated successfully!")
                    clear_contact_cache()
                    st.session_state['popup_action'] = None
                    st.session_state['popup_contact_id'] = None
                    st.session_state["action_row"] = None
                    st.session_state["action_type"] = None
                    st.experimental_rerun()
                else:
                    st.error("❌ Failed to update contact")
            except Exception as e:
                error_msg = str(e)
                show_database_error_message(error_msg)
                
        elif cancel_button:
            st.session_state['popup_action'] = None
            st.session_state['popup_contact_id'] = None
            st.session_state["action_row"] = None
            st.session_state["action_type"] = None
            st.experimental_rerun()
            
        elif reset_button:
            st.experimental_rerun()


def show_settings():
    """Tab for application settings and information."""
    
    st.markdown('<h2 class="section-header">⚙️ Application Settings</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 System Information")
        st.markdown("""
        **Application Version:** 1.0.0
        **Python Version:** 3.8+
        **Database:** MySQL
        **OCR Engine:** EasyOCR
        **Image Processing:** OpenCV
        """)
        
        st.markdown("### 📊 Performance Tips")
        st.markdown("""
        - Use high-resolution images (300+ DPI)
        - Ensure good lighting and contrast
        - Keep text clearly visible
        - Avoid blurry or distorted images
        - Use standard business card formats
        """)
    
    with col2:
        st.markdown("### 🛠️ Troubleshooting")
        st.markdown("""
        **Common Issues:**
        - Database connection failed → Check MySQL settings
        - No text extracted → Improve image quality
        - Import errors → Use the provided CSV template
        - Module errors → Activate virtual environment
        """)
        
        st.markdown("### 📞 Support")
        st.markdown("""
        **Need Help?**
        - Check the troubleshooting section
        - Review error messages carefully
        - Ensure all dependencies are installed
        - Verify database connectivity
        """)
    
    # Test system components
    st.markdown("### 🧪 System Test")
    if st.button("🔍 Run System Test", type="secondary"):
        run_system_test()


def display_extracted_data_enhanced(data):
    """Display extracted data with enhanced styling."""
    
    if not data:
        st.warning("No data to display")
        return
    
    # Display raw extracted text
    with st.expander("📝 Raw Extracted Text", expanded=False):
        st.text_area("Raw Text", value=data['raw_text'], height=150, disabled=True)
    
    # Display classified data with enhanced styling
    classified = data['classified_data']
    
    # Personal Information
    st.markdown("### 👤 Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="data-field">
            <div class="data-label">Name</div>
            <div class="data-value">{classified.get('name', 'Not found')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="data-field">
            <div class="data-label">Designation</div>
            <div class="data-value">{classified.get('designation', 'Not found')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="data-field">
            <div class="data-label">Company</div>
            <div class="data-value">{classified.get('company', 'Not found')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="data-field">
            <div class="data-label">Address</div>
            <div class="data-value">{classified.get('address', 'Not found')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact Information
    st.markdown("### 📞 Contact Information")
    
    # Phone numbers
    phones = classified.get('phone', [])
    if phones:
        st.markdown("**📱 Phone Numbers:**")
        for i, phone in enumerate(phones, 1):
            st.markdown(f"• {phone}")
    else:
        st.markdown("**📱 Phone Numbers:** Not found")
    
    # Email addresses
    emails = classified.get('email', [])
    if emails:
        st.markdown("**📧 Email Addresses:**")
        for i, email in enumerate(emails, 1):
            st.markdown(f"• {email}")
    else:
        st.markdown("**📧 Email Addresses:** Not found")
    
    # Websites
    websites = classified.get('website', [])
    if websites:
        st.markdown("**🌐 Websites:**")
        for i, website in enumerate(websites, 1):
            st.markdown(f"• {website}")
    else:
        st.markdown("**🌐 Websites:** Not found")
    
    # Display JSON format
    with st.expander("🔧 JSON Format", expanded=False):
        st.json(classified)


def clear_contact_cache():
    """Clear contact cache when data is modified."""
    get_cached_contacts.clear()

def save_to_database(data):
    """Save extracted data to database with duplicate checking."""
    
    try:
        if not data or 'classified_data' not in data:
            st.error("❌ No data available to save")
            return
        
        classified_data = data['classified_data']
        
        # Validate that we have at least a name or company
        if not classified_data.get('name') and not classified_data.get('company'):
            st.error("❌ At least a name or company is required to save")
            return
        
        # Check for duplicates before saving
        duplicate_check = db_manager.check_duplicates(classified_data)
        
        if duplicate_check['has_duplicates']:
            # Show duplicate warning with details
            st.warning("⚠️ **Potential Duplicate Contact Detected!**")
            
            # Display duplicate information
            with st.expander("🔍 View Duplicate Details", expanded=True):
                st.markdown("**The following existing contacts match the new data:**")
                
                for i, duplicate in enumerate(duplicate_check['duplicates'], 1):
                    st.markdown(f"**Duplicate {i}:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Name:** {duplicate.get('name', 'N/A')}")
                        st.markdown(f"**Company:** {duplicate.get('company', 'N/A')}")
                        st.markdown(f"**Designation:** {duplicate.get('designation', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**Phone:** {duplicate.get('phone', 'N/A')}")
                        st.markdown(f"**Email:** {duplicate.get('email', 'N/A')}")
                        st.markdown(f"**Added:** {duplicate.get('created_at', 'N/A')}")
                    
                    # Show which fields match
                    match_fields = duplicate.get('match_fields', [])
                    if match_fields:
                        st.markdown(f"**Matching fields:** {', '.join(match_fields)}")
                    
                    st.markdown("---")
                
                # Show summary of matching fields
                duplicate_fields = duplicate_check['duplicate_fields']
                st.markdown(f"**Summary:** Found {len(duplicate_check['duplicates'])} existing contact(s) with matching: {', '.join(duplicate_fields)}")
            
            # Ask user if they want to proceed
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("✅ Save Anyway", key="save_duplicate", help="Save the contact even though duplicates exist"):
                    proceed_with_save(classified_data)
            with col2:
                if st.button("❌ Cancel", key="cancel_duplicate", help="Cancel saving this contact"):
                    st.info("💡 Contact not saved. You can modify the data and try again.")
            with col3:
                if st.button("🔄 Modify Data", key="modify_duplicate", help="Go back and modify the extracted data"):
                    st.session_state['show_edit_form'] = True
                    st.rerun()
        else:
            # No duplicates found, proceed with save
            proceed_with_save(classified_data)
            
    except Exception as e:
        error_msg = str(e)
        show_database_error_message(error_msg)
        logger.error(f"Error saving to database: {e}")


def proceed_with_save(classified_data):
    """Proceed with saving the contact to database."""
    try:
        # Save to database
        success = store_in_db(classified_data)
        
        if success:
            st.success("✅ Contact saved to database successfully!")
            # Clear cache to refresh data
            clear_contact_cache()
            # Clear session state to allow new upload
            if f'extracted_data_{st.session_state.get("current_card", 0)}' in st.session_state:
                del st.session_state[f'extracted_data_{st.session_state.get("current_card", 0)}']
            st.rerun()
        else:
            st.error("❌ Failed to save contact to database")
            
    except Exception as e:
        error_msg = str(e)
        show_database_error_message(error_msg)
        logger.error(f"Error saving to database: {e}")


def export_data(format_type):
    """Export contacts to CSV or Excel."""
    
    try:
        with st.spinner(f"🔄 Exporting contacts to {format_type}..."):
            if format_type == "CSV":
                filepath = export_to_csv()
            else:  # Excel
                filepath = export_to_excel()
            
            if filepath and os.path.exists(filepath):
                # Read the file and create download button
                with open(filepath, 'rb') as f:
                    file_content = f.read()
                
                # Create download button
                st.download_button(
                    label=f"📥 Download {format_type} File",
                    data=file_content,
                    file_name=os.path.basename(filepath),
                    mime="application/octet-stream" if format_type == "Excel" else "text/csv",
                    use_container_width=True
                )
                
                st.success(f"✅ Successfully exported contacts to {format_type}")
                
                # Clean up the temporary file
                try:
                    os.unlink(filepath)
                except:
                    pass
            else:
                st.error(f"❌ Failed to export contacts to {format_type}")
                
    except Exception as e:
        error_msg = str(e)
        show_database_error_message(error_msg)
        logger.error(f"Error exporting data: {e}")


def import_data(uploaded_file, skip_duplicates):
    """Import contacts from CSV file."""
    
    try:
        with st.spinner("🔄 Importing contacts..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_csv_path = tmp_file.name
            
            # Import contacts
            result = import_from_csv(temp_csv_path, skip_duplicates)
            
            # Clean up temporary file
            try:
                os.unlink(temp_csv_path)
            except:
                pass
            
            # Display results
            if result['success_count'] > 0:
                st.success(f"✅ {result['message']}")
                st.info(f"📊 Import Summary: {result['success_count']} successful, {result['error_count']} errors out of {result['total_count']} total rows")
                
                # Clear cache to refresh data
                clear_contact_cache()
                
                if result['errors']:
                    with st.expander("⚠️ Import Errors", expanded=False):
                        for error in result['errors']:
                            st.write(f"• {error}")
            else:
                st.error(f"❌ {result['message']}")
                if result['errors']:
                    with st.expander("❌ Import Errors", expanded=True):
                        for error in result['errors']:
                            st.write(f"• {error}")
            
            # Refresh the page to show updated contacts
            st.rerun()
            
    except Exception as e:
        error_msg = str(e)
        show_database_error_message(error_msg)
        logger.error(f"Error importing data: {e}")


def run_system_test():
    """Run a system test to check all components."""
    
    st.markdown("### 🧪 Running System Tests...")
    
    # Test imports
    try:
        import cv2
        st.success("✅ OpenCV (cv2) - OK")
    except:
        st.error("❌ OpenCV (cv2) - Failed")
    
    try:
        import easyocr
        st.success("✅ EasyOCR - OK")
    except:
        st.error("❌ EasyOCR - Failed")
    
    try:
        import streamlit
        st.success("✅ Streamlit - OK")
    except:
        st.error("❌ Streamlit - Failed")
    
    try:
        import mysql.connector
        st.success("✅ MySQL Connector - OK")
    except:
        st.error("❌ MySQL Connector - Failed")
    
    try:
        import pandas
        st.success("✅ Pandas - OK")
    except:
        st.error("❌ Pandas - Failed")
    
    # Test database connection
    try:
        if db_manager.test_connection():
            st.success("✅ Database Connection - OK")
        else:
            st.error("❌ Database Connection - Failed")
    except:
        st.error("❌ Database Connection - Failed")
    
    st.success("🎉 System test completed!")


def show_database_error_message(error_msg):
    """Display user-friendly database error messages."""
    if "database" in error_msg.lower() and "does not exist" in error_msg.lower():
        st.error("""
        ❌ **Database Not Found**
        
        The database you're trying to connect to doesn't exist. Here's how to fix it:
        
        **For PostgreSQL:**
        1. Open your PostgreSQL client (pgAdmin, DBeaver, or command line)
        2. Connect to your PostgreSQL server
        3. Create a new database named `business_cards`
        4. Try connecting again
        
        **For MySQL:**
        1. Open MySQL Workbench or command line
        2. Connect to your MySQL server
        3. Run: `CREATE DATABASE business_cards;`
        4. Try connecting again
        
        **For SQLite:**
        - The database file will be created automatically
        - Make sure the directory exists and is writable
        """)
    elif "connection" in error_msg.lower() and "failed" in error_msg.lower():
        st.error("""
        ❌ **Connection Failed**
        
        Unable to connect to the database server. Please check:
        
        **Connection Settings:**
        - ✅ Host address is correct
        - ✅ Port number is correct (MySQL: 3306, PostgreSQL: 5432)
        - ✅ Username and password are correct
        - ✅ Database server is running
        
        **Common Solutions:**
        - Start your database server if it's not running
        - Check firewall settings
        - Verify network connectivity
        - Ensure the database user has proper permissions
        """)
    elif "authentication" in error_msg.lower() or "password" in error_msg.lower():
        st.error("""
        ❌ **Authentication Failed**
        
        Invalid username or password. Please check:
        
        - ✅ Username is correct
        - ✅ Password is correct
        - ✅ User has access to the specified database
        - ✅ User has proper permissions
        
        **For PostgreSQL:** Make sure the user exists and has proper privileges
        **For MySQL:** Verify the user can connect from your host
        """)
    elif "permission" in error_msg.lower() or "access" in error_msg.lower():
        st.error("""
        ❌ **Permission Denied**
        
        The database user doesn't have sufficient permissions. Please:
        
        - Grant necessary permissions to the user
        - For PostgreSQL: `GRANT ALL PRIVILEGES ON DATABASE business_cards TO username;`
        - For MySQL: `GRANT ALL PRIVILEGES ON business_cards.* TO 'username'@'host';`
        - Contact your database administrator if needed
        """)
    else:
        st.error(f"""
        ❌ **Database Error**
        
        An unexpected error occurred: `{error_msg}`
        
        **Troubleshooting Steps:**
        1. Check your database connection settings
        2. Ensure the database server is running
        3. Verify network connectivity
        4. Check database logs for more details
        5. Try connecting with a database client first
        """)


def check_existing_duplicates(contacts_df):
    """Check for duplicate contacts in the existing database."""
    
    st.markdown("### 🔍 Duplicate Detection Results")
    
    try:
        duplicates_found = []
        
        # Check for duplicates based on name, phone, and email
        for idx, contact in contacts_df.iterrows():
            contact_id = contact.get('id')
            name = str(contact.get('name', '')).strip().lower()
            phones = []
            if contact.get('phone'):
                phones = [phone.strip().lower() for phone in str(contact['phone']).split(',') if phone.strip()]
            emails = []
            if contact.get('email'):
                emails = [email.strip().lower() for email in str(contact['email']).split(',') if email.strip()]
            
            # Check against other contacts
            for other_idx, other_contact in contacts_df.iterrows():
                if idx == other_idx:  # Skip self
                    continue
                
                other_id = other_contact.get('id')
                other_name = str(other_contact.get('name', '')).strip().lower()
                other_phones = []
                if other_contact.get('phone'):
                    other_phones = [phone.strip().lower() for phone in str(other_contact['phone']).split(',') if phone.strip()]
                other_emails = []
                if other_contact.get('email'):
                    other_emails = [email.strip().lower() for email in str(other_contact['email']).split(',') if email.strip()]
                
                match_fields = []
                
                # Check name match
                if name and other_name and name == other_name:
                    match_fields.append('name')
                
                # Check phone matches
                for phone in phones:
                    for other_phone in other_phones:
                        if phone and other_phone and phone == other_phone:
                            if 'phone' not in match_fields:
                                match_fields.append('phone')
                
                # Check email matches
                for email in emails:
                    for other_email in other_emails:
                        if email and other_email and email == other_email:
                            if 'email' not in match_fields:
                                match_fields.append('email')
                
                # If any field matches, add to duplicates
                if match_fields:
                    duplicate_pair = {
                        'contact1': {
                            'id': contact_id,
                            'name': contact.get('name'),
                            'company': contact.get('company'),
                            'phone': contact.get('phone'),
                            'email': contact.get('email'),
                            'created_at': contact.get('created_at')
                        },
                        'contact2': {
                            'id': other_id,
                            'name': other_contact.get('name'),
                            'company': other_contact.get('company'),
                            'phone': other_contact.get('phone'),
                            'email': other_contact.get('email'),
                            'created_at': other_contact.get('created_at')
                        },
                        'match_fields': match_fields
                    }
                    
                    # Avoid duplicate pairs (A-B and B-A)
                    pair_key = tuple(sorted([contact_id, other_id]))
                    if pair_key not in [tuple(sorted([d['contact1']['id'], d['contact2']['id']])) for d in duplicates_found]:
                        duplicates_found.append(duplicate_pair)
        
        if duplicates_found:
            st.warning(f"⚠️ **Found {len(duplicates_found)} potential duplicate pairs!**")
            
            # Group duplicates by matching fields
            duplicate_groups = {}
            for duplicate in duplicates_found:
                match_key = tuple(sorted(duplicate['match_fields']))
                if match_key not in duplicate_groups:
                    duplicate_groups[match_key] = []
                duplicate_groups[match_key].append(duplicate)
            
            # Display duplicates grouped by matching fields
            for i, (match_fields, group) in enumerate(duplicate_groups.items(), 1):
                st.markdown(f"#### 🔍 Group {i}: Matching {', '.join(match_fields)}")
                
                for j, duplicate in enumerate(group, 1):
                    with st.expander(f"Duplicate Pair {j}", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Contact 1:**")
                            st.markdown(f"**Name:** {duplicate['contact1']['name']}")
                            st.markdown(f"**Company:** {duplicate['contact1']['company']}")
                            st.markdown(f"**Phone:** {duplicate['contact1']['phone']}")
                            st.markdown(f"**Email:** {duplicate['contact1']['email']}")
                            st.markdown(f"**Added:** {duplicate['contact1']['created_at']}")
                        
                        with col2:
                            st.markdown("**Contact 2:**")
                            st.markdown(f"**Name:** {duplicate['contact2']['name']}")
                            st.markdown(f"**Company:** {duplicate['contact2']['company']}")
                            st.markdown(f"**Phone:** {duplicate['contact2']['phone']}")
                            st.markdown(f"**Email:** {duplicate['contact2']['email']}")
                            st.markdown(f"**Added:** {duplicate['contact2']['created_at']}")
                        
                        st.markdown(f"**Matching fields:** {', '.join(duplicate['match_fields'])}")
                        
                        # Action buttons for each duplicate pair
                        action_col1, action_col2, action_col3 = st.columns(3)
                        with action_col1:
                            if st.button(f"🗑️ Delete Contact 1", key=f"del1_{i}_{j}"):
                                if delete_contact(duplicate['contact1']['id']):
                                    st.success("✅ Contact 1 deleted successfully!")
                                    clear_contact_cache()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete contact 1")
                        
                        with action_col2:
                            if st.button(f"🗑️ Delete Contact 2", key=f"del2_{i}_{j}"):
                                if delete_contact(duplicate['contact2']['id']):
                                    st.success("✅ Contact 2 deleted successfully!")
                                    clear_contact_cache()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete contact 2")
                        
                        with action_col3:
                            if st.button(f"✏️ Merge Contacts", key=f"merge_{i}_{j}"):
                                if db_manager.merge_contacts(duplicate['contact1']['id'], duplicate['contact2']['id']):
                                    st.success("✅ Contacts merged successfully!")
                                    clear_contact_cache()
                                    st.rerun()
                
                st.markdown("---")
            
            # Summary statistics
            st.markdown("### 📊 Duplicate Summary")
            total_duplicates = len(duplicates_found)
            unique_contacts_involved = set()
            for duplicate in duplicates_found:
                unique_contacts_involved.add(duplicate['contact1']['id'])
                unique_contacts_involved.add(duplicate['contact2']['id'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Duplicate Pairs", total_duplicates)
            with col2:
                st.metric("Unique Contacts Involved", len(unique_contacts_involved))
            with col3:
                st.metric("Total Contacts", len(contacts_df))
            
        else:
            st.success("✅ **No duplicates found!** Your contact database is clean.")
            
    except Exception as e:
        st.error(f"❌ Error checking for duplicates: {str(e)}")
        logger.error(f"Error checking duplicates: {e}")


if __name__ == "__main__":
    main() 