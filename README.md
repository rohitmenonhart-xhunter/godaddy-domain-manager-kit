# GoDaddy Domain Management Tool

![StellarLabs](https://img.shields.io/badge/StellarLabs-Authorized-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

A modular Python application for automating domain management tasks using the GoDaddy API. This tool allows you to check domain availability, search for domains based on keywords, and purchase domains through an interactive command-line interface.

**Developed and maintained by StellarLabs**

## Features

- ✅ **Domain Availability Check**: Quickly verify if a domain is available for registration
- ✅ **Intelligent Domain Suggestions**: Get alternative domain suggestions when your preferred domain is unavailable
- ✅ **Advanced Domain Search**: Search for domains based on keywords with customizable TLD filters
- ✅ **Seamless Purchase Flow**: Complete domain purchase process with intuitive step-by-step guidance
- ⬜ **Payment Integration**: QR code generation for UPI payments
- ✅ **Contact Information Management**: Simplified contact information collection with validation
- ✅ **Colorful User Interface**: User-friendly CLI with visual enhancements
- ✅ **Detailed Error Reporting**: Clear error messages and debugging information

## Installation

### Prerequisites

- Python 3.8 or higher
- GoDaddy API credentials (API Key and Secret)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rohitmenonhart-xhunter/godaddy-domain-manager.git
   cd godaddy-domain-manager
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your GoDaddy API credentials**:
   - Create a GoDaddy API key and secret at https://developer.godaddy.com/
   - Create a `.env` file in the project root directory with the following content:
     ```
     # GoDaddy API Credentials
     GODADDY_API_KEY=your_api_key_here
     GODADDY_API_SECRET=your_api_secret_here

     # Environment Settings
     API_URL=https://api.godaddy.com
     # For test environment use:
     # API_URL=https://api.ote-godaddy.com
     ```

## Usage

### Running the Application

Start the application with:
```bash
python main.py
```

### Main Features

1. **Check Domain Availability**
   - Enter a domain name to check its availability
   - If available, you can purchase it directly
   - If unavailable, you'll get suggestions for similar domains

2. **Search for Domains**
   - Enter a keyword to search for available domains
   - Filter by TLD categories (.com/.net/.org, tech domains, startup domains, etc.)
   - View pricing information for each available domain

3. **Purchase a Domain**
   - Select registration period (1-10 years)
   - Choose privacy protection options
   - Configure auto-renewal settings
   - Enter registrant contact information
   - Complete payment via UPI or other provided methods

### Testing Purchase Functionality

For testing domain purchases without affecting real domains:
```bash
python test_purchase.py
```
This script provides detailed feedback on the API request and response.

## Project Structure

```
godaddy-domain-manager/
├── .env                  # Environment variables (API credentials)
├── .gitignore            # Git ignore rules
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── test_purchase.py      # Debug script for testing purchases
└── src/                  # Source code
    ├── api/              # API integration modules
    │   └── godaddy_client.py  # GoDaddy API client
    ├── ui/               # User interface modules
    │   └── cli.py        # Command-line interface
    └── utils/            # Utility modules
        ├── config.py     # Configuration utilities
        └── validators.py # Validation utilities
```

## Development Guide

### Architecture

The application follows a modular architecture:

1. **API Layer** (`src/api/`): Handles all interactions with the GoDaddy API
2. **UI Layer** (`src/ui/`): Manages user interactions and display
3. **Utils** (`src/utils/`): Contains reusable utility functions and configuration

### Key Components

- **GoDaddyClient** (`src/api/godaddy_client.py`): Makes authenticated requests to the GoDaddy API
- **DomainCLI** (`src/ui/cli.py`): Implements the command-line interface and user flows
- **Validators** (`src/utils/validators.py`): Contains validation logic for domains and contact information
- **Config** (`src/utils/config.py`): Handles configuration and logging setup

### Adding New Features

To extend the application:

1. **New API Endpoints**: Add methods to `GoDaddyClient` class
2. **New User Flows**: Implement new methods in `DomainCLI` class
3. **New Validations**: Add validation functions to `validators.py`

### Testing

Manual testing can be performed using the `test_purchase.py` script which provides detailed information about API interactions.

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify your API key and secret in the `.env` file
   - Ensure you're using the correct API URL (production vs. test)

2. **Domain Purchase Failures**:
   - Check the error message for details about invalid fields
   - Verify contact information format (especially country codes)
   - For payment issues, ensure you have funds available

3. **Module Import Errors**:
   - Verify that all dependencies are installed: `pip install -r requirements.txt`
   - Ensure you're running the script from the project root directory

## API Documentation

For detailed information about the GoDaddy API:
- [GoDaddy API Documentation](https://developer.godaddy.com/doc)
- [Domains API Reference](https://developer.godaddy.com/doc/endpoint/domains)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed and maintained by StellarLabs
- Uses the GoDaddy API for domain management
- Built with Python and open-source libraries

---

© 2025 StellarLabs. All rights reserved. 