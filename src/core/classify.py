"""
Text Classification Module for Business Card Extraction
Classifies extracted text into business card fields using regex patterns and heuristics.
"""

import re
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def classify_text(text):
    """
    Classify extracted text into business card fields.
    
    Args:
        text (str): Raw text extracted from business card
        
    Returns:
        dict: Dictionary containing classified fields:
            - name: Person's name
            - designation: Job title/position
            - company: Company name
            - phone: List of phone numbers
            - email: List of email addresses
            - website: List of websites
            - address: Address information
    """
    try:
        if not text or not text.strip():
            logger.warning("Empty text provided for classification")
            return {
                'name': '',
                'designation': '',
                'company': '',
                'phone': [],
                'email': [],
                'website': [],
                'address': ''
            }
        
        # Split text into lines and clean up
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Initialize result dictionary
        result = {
            'name': '',
            'designation': '',
            'company': '',
            'phone': [],
            'email': [],
            'website': [],
            'address': ''
        }
        
        # Extract phone numbers
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_matches = re.findall(phone_pattern, text)
        result['phone'] = [match for match in phone_matches if match.strip()]
        
        # Extract email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        result['email'] = re.findall(email_pattern, text)
        
        # Extract websites
        website_pattern = r'(https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        website_matches = re.findall(website_pattern, text)
        result['website'] = [match[1] if match[0] else match[1] for match in website_matches]
        
        # Remove extracted patterns from text for further processing
        cleaned_text = re.sub(phone_pattern, '', text)
        cleaned_text = re.sub(email_pattern, '', cleaned_text)
        cleaned_text = re.sub(website_pattern, '', cleaned_text)
        
        # Split cleaned text into lines
        cleaned_lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
        
        # Heuristic-based classification
        if cleaned_lines:
            # First line is often the name
            result['name'] = cleaned_lines[0]
            
            # Look for designation keywords
            designation_keywords = [
                'manager', 'director', 'president', 'ceo', 'cto', 'cfo', 'vp', 'vice president',
                'senior', 'junior', 'lead', 'head', 'chief', 'coordinator', 'specialist',
                'analyst', 'engineer', 'developer', 'designer', 'consultant', 'advisor',
                'executive', 'officer', 'associate', 'assistant', 'supervisor', 'coordinator'
            ]
            
            # Look for company keywords
            company_keywords = [
                'inc', 'llc', 'ltd', 'corp', 'corporation', 'company', 'co', 'enterprises',
                'group', 'associates', 'partners', 'solutions', 'systems', 'technologies',
                'international', 'global', 'worldwide', 'services', 'consulting'
            ]
            
            # Classify remaining lines
            designation_lines = []
            company_lines = []
            address_lines = []
            
            for line in cleaned_lines[1:]:
                line_lower = line.lower()
                
                # Check for designation
                if any(keyword in line_lower for keyword in designation_keywords):
                    designation_lines.append(line)
                # Check for company
                elif any(keyword in line_lower for keyword in company_keywords):
                    company_lines.append(line)
                # Check for address indicators
                elif any(indicator in line_lower for indicator in ['street', 'avenue', 'road', 'drive', 'lane', 'boulevard', 'suite', 'floor', 'building']):
                    address_lines.append(line)
                # Check for postal code pattern
                elif re.search(r'\d{5}(-\d{4})?', line):
                    address_lines.append(line)
                # If line contains numbers and common address words, likely address
                elif re.search(r'\d+', line) and any(word in line_lower for word in ['st', 'ave', 'rd', 'dr', 'blvd', 'ln', 'ct', 'pl']):
                    address_lines.append(line)
                else:
                    # If not classified yet, check if it looks like a company name
                    if len(line.split()) <= 3 and not any(char.isdigit() for char in line):
                        company_lines.append(line)
                    else:
                        address_lines.append(line)
            
            # Set designation (take the first one found)
            if designation_lines:
                result['designation'] = designation_lines[0]
            
            # Set company (take the first one found)
            if company_lines:
                result['company'] = company_lines[0]
            
            # Set address (join remaining lines)
            if address_lines:
                result['address'] = ', '.join(address_lines)
        
        logger.info(f"Text classification completed. Found: {len(result['phone'])} phones, {len(result['email'])} emails, {len(result['website'])} websites")
        return result
        
    except Exception as e:
        logger.error(f"Error during text classification: {e}")
        return {
            'name': '',
            'designation': '',
            'company': '',
            'phone': [],
            'email': [],
            'website': [],
            'address': ''
        }


def validate_phone(phone):
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid phone number format
    """
    phone_pattern = r'^(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return bool(re.match(phone_pattern, phone.strip()))


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid email format
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email.strip()))


def validate_website(website):
    """
    Validate website format.
    
    Args:
        website (str): Website to validate
        
    Returns:
        bool: True if valid website format
    """
    website_pattern = r'^(https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$'
    return bool(re.match(website_pattern, website.strip()))


if __name__ == "__main__":
    # Test the classification function
    test_text = """
    John Smith
    Senior Software Engineer
    Tech Solutions Inc.
    123 Main Street, Suite 100
    New York, NY 10001
    Phone: (555) 123-4567
    Email: john.smith@techsolutions.com
    Website: www.techsolutions.com
    """
    
    result = classify_text(test_text)
    print("Classification result:")
    for key, value in result.items():
        print(f"{key}: {value}") 