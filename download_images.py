import json
import requests
import os
import time
from PIL import Image
from io import BytesIO

# Ensure directories exist
os.makedirs('static/images/products', exist_ok=True)
os.makedirs('static/images/banners', exist_ok=True)

# Load product data
with open('data/products.json', 'r') as f:
    data = json.load(f)

# Unsplash API for free stock images
# We'll use direct URLs to avoid API key requirements
image_urls = {
    # Coffee products
    "House Blend Coffee": "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=600&q=80",
    "Ethiopian Single Origin": "https://images.unsplash.com/photo-1497636577773-f1231844b336?w=600&q=80",
    "Espresso Blend": "https://images.unsplash.com/photo-1595434091143-b375ced5fe5c?w=600&q=80",
    "Colombian Decaf": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&q=80",
    "Sumatra Dark Roast": "https://images.unsplash.com/photo-1580933073521-dc49ac0d4e6a?w=600&q=80",
    
    # Equipment
    "Cold Brew Kit": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=600&q=80",
    "Pour Over Coffee Maker": "https://images.unsplash.com/photo-1579992357154-faf4bde95b3d?w=600&q=80", 
    "French Press": "https://images.unsplash.com/photo-1519897831810-a9a01aceccd1?w=600&q=80",
    
    # Hero banner
    "Hero Banner": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80"
}

# Fallback images in case the download fails
fallback_images = {
    "coffee": "static/images/products/coffee_default.jpg",
    "equipment": "static/images/products/equipment_default.jpg"
}

# Download images
def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        # Open and resize the image
        img = Image.open(BytesIO(response.content))
        if save_path == 'static/images/banners/hero.jpg':
            img = img.resize((800, 400), Image.LANCZOS)
        else:
            img = img.resize((600, 400), Image.LANCZOS)
        
        # Save the image
        img.save(save_path)
        print(f"Downloaded and saved: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Download hero image
hero_url = image_urls.get("Hero Banner")
if hero_url:
    download_image(hero_url, 'static/images/banners/hero.jpg')

# Download product images
for product in data['products']:
    product_id = product['id']
    product_name = product['name']
    category = product['category']
    
    # Get the URL for this product
    url = image_urls.get(product_name)
    
    if url:
        save_path = f'static/images/products/product_{product_id}.jpg'
        success = download_image(url, save_path)
        
        if success:
            # Update the product image path in the data
            product['image'] = f'/static/images/products/product_{product_id}.jpg'
        else:
            # Use fallback image
            product['image'] = f'/static/images/products/{category}_default.jpg'
    else:
        # No URL for this product, use fallback
        product['image'] = f'/static/images/products/{category}_default.jpg'
    
    # Avoid rate limiting
    time.sleep(0.5)

# Save updated product data
with open('data/products.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Image download complete!")