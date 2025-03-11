import json
import os
import requests
from PIL import Image
from io import BytesIO

# Load product data
with open('data/products.json', 'r') as f:
    data = json.load(f)

# Create directory if it doesn't exist
os.makedirs('static/images/products', exist_ok=True)

# Download and save images locally
for product in data['products']:
    product_id = product['id']
    image_url = product['image']
    
    try:
        # Download image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Process image with PIL
            img = Image.open(BytesIO(response.content))
            
            # Save as local file
            local_path = f'static/images/products/product_{product_id}.jpg'
            img.save(local_path)
            
            # Update JSON with local path
            product['image'] = f'/static/images/products/product_{product_id}.jpg'
            print(f"Downloaded: {product['name']} image")
        else:
            print(f"Failed to download image for {product['name']}")
    except Exception as e:
        print(f"Error processing {product['name']} image: {e}")

# Create default product images if downloads fail
coffee_default = Image.new('RGB', (600, 400), (139, 69, 19))
coffee_default.save('static/images/products/coffee_default.jpg')

equipment_default = Image.new('RGB', (600, 400), (72, 72, 72))
equipment_default.save('static/images/products/equipment_default.jpg')

# Check for any missing images and use defaults
for product in data['products']:
    local_path = f'static/images/products/product_{product["id"]}.jpg'
    if not os.path.exists(local_path):
        if product['category'] == 'coffee':
            product['image'] = '/static/images/products/coffee_default.jpg'
        else:
            product['image'] = '/static/images/products/equipment_default.jpg'
        print(f"Using default image for {product['name']}")

# Save updated product data
with open('data/products.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Image download and processing complete!")