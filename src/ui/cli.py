"""
Command-line interface for the GoDaddy Domain Management tool.
"""

import os
import sys
import time
import logging
import inquirer
import pyfiglet
from colorama import init, Fore, Style
from src.utils.validators import validate_domain_name, validate_email, validate_phone

# Initialize colorama
init(autoreset=True)

class DomainCLI:
    """Command-line interface for domain management."""
    
    def __init__(self, godaddy_client):
        """
        Initialize the CLI interface.
        
        Args:
            godaddy_client (GoDaddyClient): GoDaddy API client instance
        """
        self.godaddy_client = godaddy_client
        self.logger = logging.getLogger("domain_manager")
        self.contact_info = {}
    
    def print_header(self):
        """Print the application header."""
        os.system('cls' if os.name == 'nt' else 'clear')
        header = pyfiglet.figlet_format("GoDaddy Domain Manager", font="slant")
        print(f"{Fore.CYAN}{header}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Automate your domain registration process{Style.RESET_ALL}")
        print("-" * 80)
    
    def start(self):
        """Start the CLI interface and guide the user through the domain process."""
        self.print_header()
        
        print(f"{Fore.GREEN}Welcome to the GoDaddy Domain Manager!{Style.RESET_ALL}")
        print("This tool will help you check domain availability and purchase domains.")
        print()
        
        while True:
            print(f"{Fore.CYAN}MAIN MENU{Style.RESET_ALL}")
            print("1. Check domain availability")
            print("2. Search for domains")
            print("3. Purchase a domain")
            print("4. Exit")
            
            try:
                choice = int(input(f"{Fore.YELLOW}Enter your choice (1-4): {Style.RESET_ALL}"))
                
                if choice == 1:
                    self.check_domain_flow()
                elif choice == 2:
                    self.search_domains_flow()
                elif choice == 3:
                    self.purchase_domain_flow()
                elif choice == 4:
                    print(f"{Fore.YELLOW}Thank you for using GoDaddy Domain Manager!{Style.RESET_ALL}")
                    sys.exit(0)
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 4.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
    
    def check_domain_flow(self):
        """Flow for checking domain availability."""
        self.print_header()
        print(f"{Fore.GREEN}Domain Availability Check{Style.RESET_ALL}")
        
        while True:
            domain_name = input(f"{Fore.CYAN}Enter the domain name to check (e.g., example.com) or 'back' to return: {Style.RESET_ALL}")
            
            if domain_name.lower() == 'back':
                return
            
            if not validate_domain_name(domain_name):
                print(f"{Fore.RED}Invalid domain name format. Please try again.{Style.RESET_ALL}")
                continue
            
            print(f"{Fore.YELLOW}Checking availability for {domain_name}...{Style.RESET_ALL}")
            
            # Show a simple spinner
            for _ in range(3):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(0.5)
            print()
            
            result = self.godaddy_client.check_domain_availability(domain_name)
            
            if "error" in result:
                print(f"{Fore.RED}Error checking domain: {result['error']}{Style.RESET_ALL}")
                continue
            
            if result.get('available', False):
                price = result.get('price', 0) / 1000000  # Convert from micros to standard currency
                print(f"{Fore.GREEN}Good news! {domain_name} is available for purchase!{Style.RESET_ALL}")
                print(f"Price: ${price:.2f} per year")
                
                # Ask if user wants to purchase the domain
                purchase_action = input(f"{Fore.YELLOW}Would you like to purchase this domain? (y/n): {Style.RESET_ALL}").lower()
                
                if purchase_action == 'y':
                    self.purchase_domain_flow(domain_name)
                    break
            else:
                print(f"{Fore.RED}{domain_name} is not available.{Style.RESET_ALL}")
                
                # Get suggestions for similar domains
                print(f"{Fore.YELLOW}Getting suggestions for similar domains...{Style.RESET_ALL}")
                suggestions = self.godaddy_client.get_suggested_domains(domain_name)
                
                if suggestions and len(suggestions) > 0:
                    print(f"{Fore.GREEN}Here are some available alternatives:{Style.RESET_ALL}")
                    for i, domain in enumerate(suggestions[:5], 1):
                        price = domain.get('price', 0) / 1000000  # Convert from micros to standard currency
                        print(f"{i}. {domain['domain']} - ${price:.2f} per year")
                    
                    # Ask if user wants to purchase any of the suggested domains
                    suggestion_action = input(f"{Fore.YELLOW}Would you like to purchase any of these domains? (y/n): {Style.RESET_ALL}").lower()
                    
                    if suggestion_action == 'y':
                        while True:
                            try:
                                selected_num = input(f"{Fore.CYAN}Enter domain number to purchase (1-{len(suggestions[:5])}) or 'back' to return: {Style.RESET_ALL}")
                                
                                if selected_num.lower() == 'back':
                                    break
                                    
                                selected_idx = int(selected_num) - 1
                                if 0 <= selected_idx < len(suggestions[:5]):
                                    selected_domain = suggestions[selected_idx]['domain']
                                    self.purchase_domain_flow(selected_domain)
                                    return
                                print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(suggestions[:5])}.{Style.RESET_ALL}")
                            except ValueError:
                                print(f"{Fore.RED}Invalid input. Please enter a number or 'back'.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}No suggested domains found.{Style.RESET_ALL}")
            
            # Ask if user wants to check another domain
            check_again = input(f"{Fore.YELLOW}Would you like to check another domain? (y/n): {Style.RESET_ALL}").lower()
            
            if check_again != 'y':
                break
    
    def search_domains_flow(self):
        """Flow for searching for domains based on keywords."""
        self.print_header()
        print(f"{Fore.GREEN}Domain Search{Style.RESET_ALL}")
        
        keyword = input(f"{Fore.CYAN}Enter a keyword to search for domains (or 'back' to return): {Style.RESET_ALL}")
        
        if keyword.lower() == 'back':
            return
        
        # Get TLDs to search
        print(f"{Fore.CYAN}Select TLD options:{Style.RESET_ALL}")
        print("1. All popular TLDs")
        print("2. .com, .net, .org only")
        print("3. .io, .dev, .tech (tech domains)")
        print("4. .ai, .app, .co (startup domains)")
        print("5. Custom selection")
        
        while True:
            try:
                tld_choice = int(input(f"{Fore.YELLOW}Enter your choice (1-5): {Style.RESET_ALL}"))
                if 1 <= tld_choice <= 5:
                    break
                print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 5.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        
        # Set the TLDs based on the selection
        if tld_choice == 1:
            # All popular TLDs
            selected_tlds = []
        elif tld_choice == 2:
            # .com, .net, .org only
            selected_tlds = ['com', 'net', 'org']
        elif tld_choice == 3:
            # Tech domains
            selected_tlds = ['io', 'dev', 'tech']
        elif tld_choice == 4:
            # Startup domains
            selected_tlds = ['ai', 'app', 'co']
        else:
            # Custom selection
            custom_tlds = input(f"{Fore.CYAN}Enter TLDs separated by commas (e.g., com,net,org): {Style.RESET_ALL}")
            selected_tlds = [tld.strip() for tld in custom_tlds.split(',')]
        
        print(f"{Fore.YELLOW}Searching for domains related to '{keyword}'...{Style.RESET_ALL}")
        
        # Show a simple spinner
        for _ in range(3):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.5)
        print()
        
        results = self.godaddy_client.search_domains(keyword, tlds=selected_tlds)
        
        if "error" in results:
            print(f"{Fore.RED}Error searching domains: {results['error']}{Style.RESET_ALL}")
            return
        
        if not results or len(results) == 0:
            print(f"{Fore.YELLOW}No domains found for keyword '{keyword}'.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}Found {len(results)} domains related to '{keyword}':{Style.RESET_ALL}")
        
        # Display domains with prices
        for i, domain in enumerate(results[:10], 1):
            price = domain.get('price', 0) / 1000000  # Convert from micros to standard currency
            print(f"{i}. {domain['domain']} - ${price:.2f} per year")
        
        # Ask if user wants to purchase any of the domains
        purchase_action = input(f"{Fore.YELLOW}Would you like to purchase any of these domains? (y/n): {Style.RESET_ALL}").lower()
        
        if purchase_action == 'y':
            while True:
                try:
                    selected_num = input(f"{Fore.CYAN}Enter domain number to purchase (1-{len(results[:10])}) or 'back' to return: {Style.RESET_ALL}")
                    
                    if selected_num.lower() == 'back':
                        return
                        
                    selected_idx = int(selected_num) - 1
                    if 0 <= selected_idx < len(results[:10]):
                        selected_domain = results[selected_idx]['domain']
                        self.purchase_domain_flow(selected_domain)
                        break
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(results[:10])}.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter a number or 'back'.{Style.RESET_ALL}")
    
    def collect_contact_info(self):
        """Collect contact information for domain registration."""
        self.print_header()
        print(f"{Fore.GREEN}Contact Information{Style.RESET_ALL}")
        print("Please provide the registrant contact information for the domain:")
        
        self.contact_info = {}
        
        fields = [
            ('firstName', 'First Name'),
            ('lastName', 'Last Name'),
            ('email', 'Email Address'),
            ('phone', 'Phone Number (with country code, e.g., +1234567890)'),
            ('addressLine1', 'Address Line 1'),
            ('addressLine2', 'Address Line 2 (optional)'),
            ('city', 'City'),
            ('state', 'State/Province'),
            ('postalCode', 'Postal/ZIP Code'),
            ('country', 'Country (2-letter code, e.g., US)')
        ]
        
        for field_name, field_desc in fields:
            required = field_name != 'addressLine2'
            
            while True:
                value = input(f"{Fore.CYAN}{field_desc}: {Style.RESET_ALL}")
                
                if required and not value:
                    print(f"{Fore.RED}This field is required. Please enter a value.{Style.RESET_ALL}")
                    continue
                
                if field_name == 'email' and value and not validate_email(value):
                    print(f"{Fore.RED}Invalid email format. Please enter a valid email.{Style.RESET_ALL}")
                    continue
                    
                if field_name == 'phone' and value and not validate_phone(value):
                    print(f"{Fore.RED}Invalid phone format. Please include country code (e.g., +1234567890).{Style.RESET_ALL}")
                    continue
                    
                if field_name == 'country' and value and len(value) != 2:
                    print(f"{Fore.RED}Country code should be 2 letters (e.g., US, IN, UK).{Style.RESET_ALL}")
                    continue
                
                break
                
            self.contact_info[field_name] = value
        
        # Create contacts in the format GoDaddy expects
        # Mapping our fields to GoDaddy's expected format
        formatted_contact = {
            "nameFirst": self.contact_info.get("firstName", ""),
            "nameLast": self.contact_info.get("lastName", ""),
            "email": self.contact_info.get("email", ""),
            "phone": self.contact_info.get("phone", ""),
            "addressMailing": {
                "address1": self.contact_info.get("addressLine1", ""),
                "address2": self.contact_info.get("addressLine2", ""),
                "city": self.contact_info.get("city", ""),
                "state": self.contact_info.get("state", ""),
                "postalCode": self.contact_info.get("postalCode", ""),
                "country": self.contact_info.get("country", "US")
            }
        }
        
        # Use the same contact info for all contact types
        return {
            "contactAdmin": formatted_contact,
            "contactBilling": formatted_contact,
            "contactRegistrant": formatted_contact,
            "contactTech": formatted_contact
        }
    
    def purchase_domain_flow(self, domain_name=None):
        """
        Flow for purchasing a domain.
        
        Args:
            domain_name (str, optional): Domain name to purchase
        """
        self.print_header()
        print(f"{Fore.GREEN}Domain Purchase{Style.RESET_ALL}")
        
        if not domain_name:
            domain_name = input(f"{Fore.CYAN}Enter the domain name to purchase (e.g., example.com) or 'back' to return: {Style.RESET_ALL}")
            
            if domain_name.lower() == 'back':
                return
            
            if not validate_domain_name(domain_name):
                print(f"{Fore.RED}Invalid domain name format. Please try again.{Style.RESET_ALL}")
                return
            
            # Check availability before proceeding
            print(f"{Fore.YELLOW}Checking availability for {domain_name}...{Style.RESET_ALL}")
            result = self.godaddy_client.check_domain_availability(domain_name)
            
            if "error" in result:
                print(f"{Fore.RED}Error checking domain: {result['error']}{Style.RESET_ALL}")
                return
            
            if not result.get('available', False):
                print(f"{Fore.RED}{domain_name} is not available for purchase.{Style.RESET_ALL}")
                return
            
            price = result.get('price', 0) / 1000000  # Convert from micros to standard currency
            print(f"{Fore.GREEN}{domain_name} is available for ${price:.2f} per year.{Style.RESET_ALL}")
        
        # Ask for registration period
        print(f"{Fore.CYAN}Select registration period:{Style.RESET_ALL}")
        print("1. 1 year")
        print("2. 2 years")
        print("3. 3 years")
        print("4. 5 years")
        print("5. 10 years")
        
        while True:
            try:
                period_choice = int(input("Enter your choice (1-5): "))
                if 1 <= period_choice <= 5:
                    break
                print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 5.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        
        period_options = {1: 1, 2: 2, 3: 3, 4: 5, 5: 10}
        period = period_options[period_choice]
        
        # Ask for privacy protection
        print(f"{Fore.CYAN}Would you like to add privacy protection?{Style.RESET_ALL}")
        print("1. Yes, protect my personal information")
        print("2. No, make my information public")
        
        while True:
            try:
                privacy_choice = int(input("Enter your choice (1-2): "))
                if 1 <= privacy_choice <= 2:
                    break
                print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        
        privacy = privacy_choice == 1
        
        # Ask for auto-renewal
        print(f"{Fore.CYAN}Would you like to enable auto-renewal?{Style.RESET_ALL}")
        print("1. Yes, automatically renew this domain")
        print("2. No, I will renew manually")
        
        while True:
            try:
                renew_choice = int(input("Enter your choice (1-2): "))
                if 1 <= renew_choice <= 2:
                    break
                print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        
        auto_renew = renew_choice == 1
        
        # Collect contact information
        contact_info = self.collect_contact_info()
        
        # Prepare purchase options
        purchase_options = {
            "period": period,
            "renewAuto": auto_renew,
            "privacy": privacy
        }
        
        # Add contact information
        for key, value in contact_info.items():
            purchase_options[key] = value
        
        # Confirm purchase
        self.print_header()
        print(f"{Fore.GREEN}Purchase Confirmation{Style.RESET_ALL}")
        print(f"You are about to purchase {Fore.CYAN}{domain_name}{Style.RESET_ALL} with the following options:")
        print(f"- Registration Period: {period} year(s)")
        print(f"- Privacy Protection: {'Enabled' if privacy else 'Disabled'}")
        print(f"- Auto-Renewal: {'Enabled' if auto_renew else 'Disabled'}")
        print(f"- Registrant: {self.contact_info['firstName']} {self.contact_info['lastName']}")
        
        confirm = input(f"{Fore.YELLOW}Do you want to proceed with the purchase? (y/n): {Style.RESET_ALL}").lower()
        
        if confirm != 'y':
            print(f"{Fore.YELLOW}Purchase cancelled.{Style.RESET_ALL}")
            return
        
        # Process purchase
        print(f"{Fore.YELLOW}Processing purchase...{Style.RESET_ALL}")
        result = self.godaddy_client.purchase_domain(domain_name, purchase_options)
        
        if "error" in result:
            error_details = result["error"]
            print(f"{Fore.RED}Error purchasing domain:{Style.RESET_ALL}")
            
            # Try to provide more detailed error information
            if isinstance(error_details, dict):
                if "fields" in error_details:
                    print(f"{Fore.RED}Invalid fields in request:{Style.RESET_ALL}")
                    for field, issue in error_details["fields"].items():
                        print(f"- {field}: {issue}")
                elif "message" in error_details:
                    print(f"{Fore.RED}{error_details['message']}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{error_details}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{error_details}{Style.RESET_ALL}")
                
            print("\nPlease check your input and try again.")
            return
            
        # Handle payment flow
        if "status" in result and result["status"] == "pending_payment":
            self.show_payment_url(result.get('paymentUrl', ''), result.get('orderId', 'N/A'))
            return
        
        # Also handle if paymentUrl is directly in the response
        if "paymentUrl" in result:
            self.show_payment_url(result["paymentUrl"], result.get('orderId', 'N/A'))
            return
        
        # Display success message
        self.print_header()
        print(f"{Fore.GREEN}Congratulations!{Style.RESET_ALL}")
        print(f"You have successfully purchased {Fore.CYAN}{domain_name}{Style.RESET_ALL}!")
        print(f"{Fore.YELLOW}Order ID: {result.get('orderId', 'N/A')}{Style.RESET_ALL}")
        print(f"The domain will be active for {period} year(s).")
        print()
        print(f"Thank you for using GoDaddy Domain Manager!")
        
        input("Press Enter to continue...")

    def show_payment_url(self, payment_url, order_id):
        """
        Display payment information to the user.
        
        Args:
            payment_url (str): URL for payment
            order_id (str): Order ID
        """
        self.print_header()
        print(f"{Fore.GREEN}Payment Required{Style.RESET_ALL}")
        print(f"Order ID: {order_id}")
        print("\nPlease complete your payment using one of the following methods:")
        print(f"\n1. Open this URL in your browser: {Fore.CYAN}{payment_url}{Style.RESET_ALL}")
        print("\n2. Scan this QR code with your UPI app:")
        
        try:
            # Try to generate a QR code if qrcode module is available
            import qrcode
            from io import StringIO
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(payment_url)
            qr.make(fit=True)
            
            # Create a string buffer to capture the ASCII art
            buffer = StringIO()
            qr.print_ascii(out=buffer)
            buffer.seek(0)
            
            # Print the QR code as ASCII art
            print("\n" + buffer.read())
        except ImportError:
            print(f"\n{Fore.YELLOW}QR code module not available. Please manually visit the URL.{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}After completing the payment, your domain will be registered.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You can check the status in your GoDaddy account.{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...") 