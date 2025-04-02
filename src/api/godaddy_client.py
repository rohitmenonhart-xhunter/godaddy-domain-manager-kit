"""
GoDaddy API client for interacting with the GoDaddy API.
"""

import requests
import logging
import json
import time

class GoDaddyClient:
    """Client for interacting with the GoDaddy API."""
    
    def __init__(self, api_key, api_secret, api_url="https://api.godaddy.com"):
        """
        Initialize the GoDaddy API client.
        
        Args:
            api_key (str): GoDaddy API key
            api_secret (str): GoDaddy API secret
            api_url (str): GoDaddy API base URL
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url
        self.api_version = "v1"
        self.logger = logging.getLogger("domain_manager")
        
        # Session for connection pooling and reuse
        self.session = requests.Session()
        
        # Set default headers for all requests
        self.session.headers.update({
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def __del__(self):
        """Clean up resources when the object is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()
    
    def _make_request(self, method, endpoint, data=None, params=None):
        """
        Make a request to the GoDaddy API.
        
        Args:
            method (str): HTTP method to use
            endpoint (str): API endpoint
            data (dict, optional): Data to send in the request
            params (dict, optional): Query parameters
            
        Returns:
            dict: Response data or error
        """
        # Ensure API URL has https:// prefix and no trailing slash
        api_url = self.api_url
        if not api_url.startswith("http"):
            api_url = f"https://{api_url}"
        api_url = api_url.rstrip("/")
        
        url = f"{api_url}/{self.api_version}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, json=data, params=params)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params)
            else:
                self.logger.error(f"Unsupported HTTP method: {method}")
                return {"error": f"Unsupported HTTP method: {method}"}
            
            # Check for successful response
            response.raise_for_status()
            
            # Return JSON response if content exists
            if response.text:
                return response.json()
            return {"success": True}
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            
            # Try to parse the error response
            try:
                error_data = response.json()
                return {"error": error_data}
            except:
                return {"error": str(e)}
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error occurred: {e}")
            return {"error": str(e)}
    
    def check_domain_availability(self, domain):
        """
        Check if a domain is available for purchase.
        
        Args:
            domain (str): Domain name to check
            
        Returns:
            dict: Domain availability information
        """
        self.logger.info(f"Checking availability for domain: {domain}")
        endpoint = f"domains/available"
        params = {"domain": domain}
        
        return self._make_request("GET", endpoint, params=params)
    
    def search_domains(self, keyword, tlds=None, suggestions=True):
        """
        Search for available domains based on a keyword.
        
        Args:
            keyword (str): Keyword to search for
            tlds (list, optional): List of TLDs to search
            suggestions (bool): Whether to include domain suggestions
            
        Returns:
            dict: Domain search results
        """
        self.logger.info(f"Searching domains with keyword: {keyword}")
        
        endpoint = "domains/suggest"
        params = {
            "query": keyword,
            "limit": 20,
            "waitMs": 1000
        }
        
        if tlds:
            params["tlds"] = ",".join(tlds)
        
        return self._make_request("GET", endpoint, params=params)
    
    def get_domain_details(self, domain):
        """
        Get details for a specific domain.
        
        Args:
            domain (str): Domain name
            
        Returns:
            dict: Domain details
        """
        self.logger.info(f"Getting details for domain: {domain}")
        endpoint = f"domains/{domain}"
        
        return self._make_request("GET", endpoint)
    
    def purchase_domain(self, domain, purchase_options):
        """
        Purchase a domain.
        
        Args:
            domain (str): Domain name to purchase
            purchase_options (dict): Domain purchase options including:
                - consent
                - period
                - nameServers
                - renewAuto
                - privacy
                - contactAdmin, contactBilling, contactRegistrant, contactTech
            
        Returns:
            dict: Purchase result
        """
        self.logger.info(f"Purchasing domain: {domain}")
        
        # Format data according to GoDaddy API requirements
        # https://developer.godaddy.com/doc/endpoint/domains#/v1/purchase
        data = {
            "domain": domain,
            "consent": {
                "agreementKeys": ["DNRA"],
                "agreedBy": purchase_options.get("agreedBy", "127.0.0.1"),
                "agreedAt": purchase_options.get("agreedAt", int(time.time() * 1000))
            },
            "period": purchase_options.get("period", 1),
            "renewAuto": purchase_options.get("renewAuto", True),
            "privacy": purchase_options.get("privacy", True)
        }
        
        # Format and add contact information
        contact_types = ["contactAdmin", "contactBilling", "contactRegistrant", "contactTech"]
        for contact_type in contact_types:
            if contact_type in purchase_options:
                contact_info = purchase_options[contact_type]
                
                # Convert from our format to GoDaddy's expected format
                formatted_contact = {
                    "nameFirst": contact_info.get("firstName", ""),
                    "nameLast": contact_info.get("lastName", ""),
                    "email": contact_info.get("email", ""),
                    "phone": contact_info.get("phone", ""),
                    "addressMailing": {
                        "address1": contact_info.get("addressLine1", ""),
                        "address2": contact_info.get("addressLine2", ""),
                        "city": contact_info.get("city", ""),
                        "state": contact_info.get("state", ""),
                        "postalCode": contact_info.get("postalCode", ""),
                        "country": contact_info.get("country", "US")
                    }
                }
                
                # Add to data
                data[contact_type] = formatted_contact
        
        # Add nameServers if provided
        if "nameServers" in purchase_options:
            data["nameServers"] = purchase_options["nameServers"]
            
        # Initiate purchase
        endpoint = "domains/purchase"
        
        # Log the request for debugging
        self.logger.debug(f"Purchase request: {json.dumps(data)}")
        
        # Make initial purchase request
        result = self._make_request("POST", endpoint, data=data)
        
        if "error" in result:
            self.logger.error(f"Domain purchase error: {result['error']}")
            return result
            
        # For UPI payment flow, we need to return the payment URL and orderId to the user
        if "paymentUrl" in result:
            self.logger.info(f"Payment URL generated: {result['paymentUrl']}")
            print(f"\nPlease complete payment at: {result['paymentUrl']}")
            print("Scan the QR code with your UPI app to complete the purchase.")
            
            # In a real application, we would now poll for payment status
            # For now, we'll just return the payment information
            return {
                "status": "pending_payment",
                "orderId": result.get("orderId", ""),
                "paymentUrl": result.get("paymentUrl", ""),
                "message": "Please complete the payment to finalize domain purchase"
            }
            
        return result

    # Add a new method to check order status
    def check_order_status(self, order_id):
        """
        Check the status of a domain order.
        
        Args:
            order_id (str): Order ID to check
            
        Returns:
            dict: Order status information
        """
        self.logger.info(f"Checking status for order: {order_id}")
        endpoint = f"orders/{order_id}"
        
        return self._make_request("GET", endpoint)
    
    def get_suggested_domains(self, domain_name, tlds=None, limit=5):
        """
        Get suggested domains similar to the provided domain name.
        
        Args:
            domain_name (str): Base domain name
            tlds (list, optional): List of TLDs to include
            limit (int): Maximum number of suggestions
            
        Returns:
            list: List of suggested domains
        """
        self.logger.info(f"Getting suggested domains for: {domain_name}")
        
        endpoint = "domains/suggest"
        
        # Extract the keyword from the domain name (remove TLD)
        keyword = domain_name.split('.')[0]
        
        params = {
            "query": keyword,
            "limit": limit
        }
        
        if tlds:
            params["tlds"] = ",".join(tlds)
        
        result = self._make_request("GET", endpoint, params=params)
        
        if "error" in result:
            return []
            
        return result 