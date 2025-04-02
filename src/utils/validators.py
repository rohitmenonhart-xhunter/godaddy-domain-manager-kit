"""
Validation utilities for the GoDaddy Domain Management tool.
"""

import re
import validators

def validate_domain_name(domain):
    """
    Validate a domain name format.
    
    Args:
        domain (str): The domain name to validate
        
    Returns:
        bool: True if the domain name is valid, False otherwise
    """
    # Basic validation first
    if not domain or len(domain) > 253:
        return False
    
    # Use validators library as primary validation
    if validators.domain(domain):
        return True
    
    # Additional validation for specific cases
    # Domain name regex pattern (simplified)
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]$"
    
    return bool(re.match(pattern, domain))

def validate_contact_info(contact_info):
    """
    Validate contact information for domain registration.
    
    Args:
        contact_info (dict): Contact information dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = [
        "firstName", "lastName", "email", "phone",
        "addressLine1", "city", "state", "postalCode", "country"
    ]
    
    for field in required_fields:
        if field not in contact_info or not contact_info[field]:
            return False, f"Missing required field: {field}"
    
    # Validate email
    if not validators.email(contact_info["email"]):
        return False, "Invalid email address"
    
    # Validate phone number (basic validation)
    phone_pattern = r"^\+?[0-9]{10,15}$"
    if not re.match(phone_pattern, contact_info["phone"]):
        return False, "Invalid phone number format"
    
    return True, ""

def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if the email is valid, False otherwise
    """
    if not email:
        return False
        
    # Use validators library if available
    try:
        import validators
        return validators.email(email)
    except (ImportError, AttributeError):
        # Fallback to regex validation
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

def validate_phone(phone):
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if the phone number is valid, False otherwise
    """
    if not phone:
        return False
        
    import re
    # Basic international phone number format with optional + prefix
    pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(pattern, phone)) 