"""
CSS Styles for Business Card Extractor
=====================================

This module contains all the CSS styling for the Streamlit application.
"""

def get_css_styles():
    """Return the CSS styles for the application."""
    return """
    <style>
        /* Desktop/laptop: center content, max width */
        .block-container {
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
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
        .card {
            background: #fff;
            color: #212529;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #1f77b4;
            width: 100%;
            box-sizing: border-box;
        }
        .card * {
            color: #212529 !important;
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
        .stButton > button {
            border-radius: 20px;
            font-weight: 600;
            padding: 0.5rem 2rem;
            border: none;
            transition: all 0.3s ease;
            min-height: 44px;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
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
        .section-header {
            font-size: clamp(1.5rem, 4vw, 1.8rem);
            color: #2c3e50;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #1f77b4;
            font-weight: 600;
        }
        .feature-highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
            font-size: clamp(0.9rem, 2.5vw, 1rem);
        }
        /* Make tables horizontally scrollable on mobile */
        .stDataFrame, .stTable {
            overflow-x: auto !important;
            width: 100% !important;
            display: block !important;
        }
        /* Responsive tweaks for mobile */
        @media (max-width: 768px) {
            .block-container {
                max-width: 100% !important;
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }
            .main-header {
                font-size: 1.5rem;
                margin-bottom: 0.5rem;
            }
            .sub-header {
                font-size: 1rem;
                margin-bottom: 1rem;
            }
            .section-header {
                font-size: 1.2rem;
                margin: 1rem 0 0.5rem 0;
                padding-bottom: 0.25rem;
            }
            .card {
                padding: 0.75rem;
                margin-bottom: 0.5rem;
                border-radius: 8px;
            }
            .feature-highlight {
                padding: 0.5rem;
                font-size: 0.9rem;
                border-radius: 8px;
            }
            .stButton > button {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
                min-height: 40px;
            }
            .progress-step {
                width: 22px;
                height: 22px;
                line-height: 22px;
                font-size: 0.9rem;
                margin-right: 6px;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.2rem !important;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 0.3rem 0.7rem !important;
                font-size: 0.9rem !important;
            }
            .stDataFrame, .stTable {
                font-size: 0.8rem;
            }
            .stMarkdown, .stFileUploader, .stCameraInput {
                margin-bottom: 0.5rem !important;
            }
        }
        @media (max-width: 480px) {
            .main-header {
                font-size: 1.1rem;
            }
            .sub-header {
                font-size: 0.8rem;
            }
            .section-header {
                font-size: 1rem;
            }
            .card {
                padding: 0.5rem;
                border-radius: 6px;
            }
            .feature-highlight {
                font-size: 0.8rem;
                padding: 0.3rem;
            }
            .progress-step {
                width: 16px;
                height: 16px;
                line-height: 16px;
                font-size: 0.7rem;
                margin-right: 4px;
            }
            .stButton > button {
                font-size: 0.8rem;
                min-height: 36px;
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
        
        .progress-steps-row {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 1rem;
        }
        @media (max-width: 768px) {
            .progress-steps-row {
                width: 100%;
                gap: 2px;
            }
            .progress-steps-row > div {
                flex: 1 1 0;
                min-width: 0;
            }
        }
    </style>
    """ 