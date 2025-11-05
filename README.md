
## Overview
This is a Django-based ecommerce project that allows users to browse product and manage their orders. 

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

5. Seed the database with initial data:
   ```
   python seed_data.py
    ```

6. Create a superuser for admin access:
    ```
    python manage.py createsuperuser
    ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.
