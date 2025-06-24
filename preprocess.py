"""
Image Preprocessing Module for Business Card Extraction
Handles image preprocessing operations using OpenCV to improve OCR accuracy.
"""

import cv2
import numpy as np
import os
import time
from pathlib import Path


def preprocess_image(image_path):
    """
    Preprocess an image for better OCR results.
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        tuple: (preprocessed_image, output_path)
            - preprocessed_image: numpy array of the processed image
            - output_path: path where the preprocessed image is saved
            
    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the image format is not supported
        Exception: For other image processing errors
    """
    try:
        # Check if input file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Create temp directory if it doesn't exist
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to load image: {image_path}")
        
        # Get original dimensions
        height, width = image.shape[:2]
        
        # Resize image (1.5x scaling for better OCR)
        scale_factor = 1.5
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding to handle varying lighting conditions
        threshold_image = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Reduce noise using morphological operations
        kernel = np.ones((1, 1), np.uint8)
        denoised_image = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, kernel)
        
        # Apply slight blur to reduce noise further
        final_image = cv2.GaussianBlur(denoised_image, (1, 1), 0)
        
        # Generate unique filename using timestamp
        timestamp = int(time.time())
        filename = f"preprocessed_{timestamp}.jpg"
        output_path = temp_dir / filename
        
        # Save the preprocessed image
        cv2.imwrite(str(output_path), final_image)
        
        return final_image, str(output_path)
        
    except FileNotFoundError as e:
        print(f"File error: {e}")
        raise
    except ValueError as e:
        print(f"Value error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during image preprocessing: {e}")
        raise


def cleanup_temp_files():
    """
    Clean up temporary files in the temp directory.
    """
    try:
        temp_dir = Path("temp")
        if temp_dir.exists():
            for file in temp_dir.glob("preprocessed_*.jpg"):
                file.unlink()
            print("Temporary files cleaned up successfully")
    except Exception as e:
        print(f"Error cleaning up temporary files: {e}")


if __name__ == "__main__":
    # Test the preprocessing function
    test_image_path = "test_card.jpg"
    if os.path.exists(test_image_path):
        try:
            processed_image, output_path = preprocess_image(test_image_path)
            print(f"Image preprocessed successfully. Output saved to: {output_path}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Test image {test_image_path} not found") 