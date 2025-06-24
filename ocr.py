"""
OCR Module for Business Card Extraction
Uses EasyOCR to extract text from preprocessed business card images.
"""

import easyocr
import os
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text(image_path):
    """
    Extract text from an image using EasyOCR.
    
    Args:
        image_path (str): Path to the preprocessed image
        
    Returns:
        str: Extracted text joined with newlines
        
    Raises:
        FileNotFoundError: If the image file doesn't exist
        Exception: For OCR processing errors
    """
    try:
        # Check if input file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Initialize EasyOCR reader (English language, GPU optional)
        logger.info("Initializing EasyOCR reader...")
        reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if CUDA is available
        
        # Read text from image
        logger.info(f"Extracting text from: {image_path}")
        results = reader.readtext(image_path)
        
        # Extract text from results
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Filter out low confidence results
                extracted_text.append(text.strip())
        
        # Join all extracted text with newlines
        full_text = '\n'.join(extracted_text)
        
        if not full_text.strip():
            logger.warning("No text was extracted from the image")
            return ""
        
        logger.info(f"Successfully extracted {len(extracted_text)} text blocks")
        return full_text
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during OCR processing: {e}")
        raise


def extract_text_with_confidence(image_path, confidence_threshold=0.5):
    """
    Extract text with confidence scores from an image.
    
    Args:
        image_path (str): Path to the preprocessed image
        confidence_threshold (float): Minimum confidence score (0.0 to 1.0)
        
    Returns:
        list: List of tuples (text, confidence_score)
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image_path)
        
        # Filter results by confidence threshold
        filtered_results = []
        for (bbox, text, confidence) in results:
            if confidence >= confidence_threshold:
                filtered_results.append((text.strip(), confidence))
        
        return filtered_results
        
    except Exception as e:
        logger.error(f"Error during OCR processing with confidence: {e}")
        raise


if __name__ == "__main__":
    # Test the OCR function
    test_image_path = "temp/preprocessed_test.jpg"
    if os.path.exists(test_image_path):
        try:
            extracted_text = extract_text(test_image_path)
            print("Extracted text:")
            print(extracted_text)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Test image {test_image_path} not found") 