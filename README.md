# Ecommerce Project

## Overview
This is a Django-based ecommerce project that allows users to browse products, manage their orders, and make payments. The project is structured into several apps, each handling different aspects of the ecommerce functionality.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ecommerce_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## Features
- User authentication (registration, login)
- Product browsing (list and detail views)
- Shopping cart management
- Order processing and payment handling
- Product reviews and ratings

## Bootstrap Integration
The project uses Bootstrap CSS for styling. Ensure that the base template (`templates/base.html`) includes the Bootstrap CDN link for proper styling of the application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.