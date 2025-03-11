import os
import json
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from forms import LoginForm, RegisterForm, CheckoutForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load products data
def load_products():
    try:
        with open('data/products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default products if file doesn't exist
        default_products = {
            "products": [
                {
                    "id": 1,
                    "name": "House Blend Coffee",
                    "description": "Our signature blend with notes of chocolate and caramel.",
                    "price": 12.99,
                    "image": "https://images.unsplash.com/photo-1610889556528-9a770e32642f?w=600",
                    "category": "coffee",
                    "featured": True
                },
                {
                    "id": 2,
                    "name": "Ethiopian Single Origin",
                    "description": "Light roasted with bright, fruity notes.",
                    "price": 15.99,
                    "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600",
                    "category": "coffee",
                    "featured": True
                },
                {
                    "id": 3,
                    "name": "Espresso Blend",
                    "description": "Dark roasted for perfect espresso extraction.",
                    "price": 14.99,
                    "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600",
                    "category": "coffee",
                    "featured": False
                },
                {
                    "id": 4,
                    "name": "Cold Brew Kit",
                    "description": "Everything you need to make smooth cold brew at home.",
                    "price": 24.99,
                    "image": "https://images.unsplash.com/photo-1560704429-519e33a6e848?w=600",
                    "category": "equipment",
                    "featured": True
                },
                {
                    "id": 5,
                    "name": "Pour Over Coffee Maker",
                    "description": "Classic glass pour over with wooden collar.",
                    "price": 29.99,
                    "image": "https://images.unsplash.com/photo-1544352453-3ba9da525950?w=600",
                    "category": "equipment",
                    "featured": False
                },
                {
                    "id": 6,
                    "name": "Colombian Decaf",
                    "description": "Full-bodied decaf with notes of caramel and nuts.",
                    "price": 13.99,
                    "image": "https://images.unsplash.com/photo-1556742393-d75f468bfcb0?w=600",
                    "category": "coffee",
                    "featured": False
                }
            ]
        }
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Save default products
        with open('data/products.json', 'w') as f:
            json.dump(default_products, f, indent=4)
            
        return default_products

# In-memory user storage (should be replaced with a database in production)
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Routes
@app.route('/')
def index():
    products_data = load_products()
    featured_products = [p for p in products_data["products"] if p.get("featured", False)]
    return render_template('index.html', products=featured_products)

@app.route('/products')
def products():
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')
    
    products_data = load_products()["products"]
    
    # Filter products by search query and category
    if search_query:
        products_data = [p for p in products_data if search_query.lower() in p["name"].lower() or 
                         search_query.lower() in p["description"].lower()]
    
    if category:
        products_data = [p for p in products_data if p["category"] == category]
        
    return render_template('products.html', products=products_data, search=search_query, category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    products_data = load_products()["products"]
    product = next((p for p in products_data if p["id"] == product_id), None)
    
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('products'))
        
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = next((users[user_id] for user_id in users if users[user_id].email == email), None)
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if username or email already exists
        if any(users[user_id].username == username for user_id in users):
            flash('Username already exists', 'danger')
            return render_template('register.html', form=form)
            
        if any(users[user_id].email == email for user_id in users):
            flash('Email already exists', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user_id = str(len(users) + 1)
        new_user = User()
        new_user.id = user_id
        new_user.username = username
        new_user.email = email
        new_user.password_hash = generate_password_hash(password)
        
        users[user_id] = new_user
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    
    if form.validate_on_submit():
        # Process checkout (in a real app, you would process payment, etc.)
        # Clear the cart
        session['cart'] = []
        flash('Order completed successfully!', 'success')
        return redirect(url_for('confirmation'))
    
    return render_template('checkout.html', form=form)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# API routes for cart functionality
@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart = session.get('cart', [])
    return {"cart": cart}

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    cart = session.get('cart', [])
    
    data = request.json
    product_id = data.get('id')
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity', 1)
    
    # Check if product already in cart
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            session['cart'] = cart
            return {"success": True, "cart": cart}
    
    # If not in cart, add it
    cart.append({
        'id': product_id,
        'name': name,
        'price': price,
        'quantity': quantity
    })
    
    session['cart'] = cart
    return {"success": True, "cart": cart}

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    cart = session.get('cart', [])
    data = request.json
    
    product_id = data.get('id')
    quantity = data.get('quantity', 0)
    
    if quantity <= 0:
        # Remove item from cart
        cart = [item for item in cart if item['id'] != product_id]
    else:
        # Update quantity
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] = quantity
                break
    
    session['cart'] = cart
    return {"success": True, "cart": cart}

@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return {"success": True, "cart": []}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
