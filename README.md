# Coffee Shop E-commerce Website

A full-featured e-commerce platform for a specialty coffee shop built with Flask.

## Features

- Product catalog with coffee beans and brewing equipment
- Shopping cart functionality with persistence
- User authentication (login/register)
- Secure checkout process
- Responsive design using Bootstrap

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms

## Setup and Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/coffee-shop.git
   cd coffee-shop
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Set environment variables
   ```
   export FLASK_APP=main.py
   export FLASK_ENV=development
   ```

4. Run the application
   ```
   flask run
   ```
   
## Product Images

The product images are sourced from Unsplash, a free stock image platform. The `download_images.py` script is used to fetch these images.

## Pricing

All prices are in Indian Rupees (₹).

## License

This project is licensed under the MIT License - see the LICENSE file for details.