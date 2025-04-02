#!/usr/bin/env python3
"""
Debug script to test the GoDaddy domain purchase API directly.

This script will attempt to purchase a domain and provide detailed debugging information.
It makes the direct API call with a properly formatted request body according to GoDaddy
documentation.
"""

import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_credentials():
    """Get API credentials from environment variables."""
    api_key = os.getenv("GODADDY_API_KEY")
    api_secret = os.getenv("GODADDY_API_SECRET")
    api_url = os.getenv("API_URL", "https://api.ote-godaddy.com")
    
    if not api_key or not api_secret:
        print("Error: API credentials not found in .env file")
        sys.exit(1)
    
    return api_key, api_secret, api_url

def check_domain_availability(api_key, api_secret, api_url, domain_name):
    """Check if a domain is available for purchase."""
    url = f"https://{api_url}/v1/domains/available"
    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    params = {"domain": domain_name}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking domain availability: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"Response: {e.response.json()}")
            except:
                print(f"Response: {e.response.text}")
        return {"error": str(e)}

def purchase_domain(api_key, api_secret, api_url, domain_name):
    """Attempt to purchase a domain with detailed error reporting."""
    url = f"https://{api_url}/v1/domains/purchase"
    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Create test contact info in the format expected by GoDaddy API
    contact_info = {
        "nameFirst": "Test",
        "nameLast": "User",
        "email": "test@example.com",
        "phone": "+11234567890",
        "addressMailing": {
            "address1": "123 Test St",
            "address2": "",
            "city": "Test City",
            "state": "TS",
            "postalCode": "12345",
            "country": "US"
        }
    }
    
    # Format data according to GoDaddy API requirements
    # Reference: https://developer.godaddy.com/doc/endpoint/domains#/v1/purchase
    data = {
        "domain": domain_name,
        "consent": {
            "agreementKeys": ["DNRA"],
            "agreedBy": "127.0.0.1",
            "agreedAt": int(time.time() * 1000)
        },
        "period": 1,
        "renewAuto": True,
        "privacy": True,
        "contactAdmin": contact_info,
        "contactBilling": contact_info,
        "contactRegistrant": contact_info,
        "contactTech": contact_info
    }
    
    print("\n=== REQUEST DETAILS ===")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Request Body: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print("\n=== RESPONSE DETAILS ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        try:
            response_json = response.json()
            print(f"Response Body: {json.dumps(response_json, indent=2)}")
            return response_json
        except json.JSONDecodeError:
            print(f"Response Body (text): {response.text}")
            return {"error": "Invalid JSON response"}
            
    except requests.exceptions.RequestException as e:
        print(f"Error purchasing domain: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"Response: {e.response.json()}")
            except:
                print(f"Response: {e.response.text}")
        return {"error": str(e)}

def main():
    """Main function to test domain purchase."""
    api_key, api_secret, api_url = get_api_credentials()
    
    print(f"Using API URL: {api_url}")
    print(f"API Key: {api_key[:5]}...{api_key[-3:]}")
    
    # Get domain name from command line or prompt
    if len(sys.argv) > 1:
        domain_name = sys.argv[1]
    else:
        domain_name = input("Enter a domain name to purchase (e.g., example.com): ")
    
    # Check domain availability first
    print(f"\nChecking availability for {domain_name}...")
    result = check_domain_availability(api_key, api_secret, api_url, domain_name)
    
    if "error" in result:
        print(f"Error checking domain: {result['error']}")
        return
    
    if not result.get('available', False):
        print(f"{domain_name} is not available for purchase.")
        return
    
    price = result.get('price', 0) / 1000000  # Convert from micros to standard currency
    print(f"{domain_name} is available for ${price:.2f} per year.")
    
    # Confirm purchase
    confirm = input(f"Would you like to attempt to purchase {domain_name}? (y/n): ").lower()
    if confirm != 'y':
        print("Purchase cancelled.")
        return
    
    # Attempt to purchase domain
    print(f"\nAttempting to purchase {domain_name}...")
    result = purchase_domain(api_key, api_secret, api_url, domain_name)
    
    if "error" in result:
        print(f"\nError purchasing domain: {result['error']}")
    else:
        print(f"\nPurchase initiated!")
        if "paymentUrl" in result:
            print(f"Payment URL: {result['paymentUrl']}")
            print("Please complete payment at the URL above.")
        print(f"Order ID: {result.get('orderId', 'N/A')}")

if __name__ == "__main__":
    main() 