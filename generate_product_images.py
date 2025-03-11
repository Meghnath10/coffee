import json
from PIL import Image, ImageDraw, ImageFont
import os

# Ensure directory exists
os.makedirs('static/images/products', exist_ok=True)

# Load product data
with open('data/products.json', 'r') as f:
    data = json.load(f)

# Create better product images
def create_coffee_image(product_id, product_name, color=(139, 69, 19)):
    """Create a nicely styled image for coffee products"""
    img = Image.new('RGB', (600, 400), color)
    draw = ImageDraw.Draw(img)
    
    # Draw a coffee bean shape
    center_x, center_y = 300, 200
    
    # Draw a coffee cup
    draw.ellipse((center_x-100, center_y+50, center_x+100, center_y+150), fill=(255, 255, 255, 128))
    draw.rectangle((center_x-100, center_y-50, center_x+100, center_y+100), fill=(255, 255, 255, 128))
    draw.ellipse((center_x-80, center_y-80, center_x+80, center_y-20), fill=(220, 220, 220))
    
    # Add steam
    for i in range(3):
        x_offset = i * 30 - 30
        draw.arc((center_x+x_offset, center_y-150, center_x+x_offset+60, center_y-100), 
                 start=180, end=0, fill=(255, 255, 255), width=5)
    
    # Add product name
    try:
        # Try to use a default font
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
        draw.text((50, 320), product_name, fill=(255, 255, 255), font=font)
    except:
        # Fallback - no custom font
        draw.text((50, 320), product_name, fill=(255, 255, 255))
    
    # Save the image
    image_path = f'static/images/products/product_{product_id}.jpg'
    img.save(image_path)
    return image_path

def create_equipment_image(product_id, product_name, color=(72, 72, 72)):
    """Create a nicely styled image for coffee equipment"""
    img = Image.new('RGB', (600, 400), color)
    draw = ImageDraw.Draw(img)
    
    # Draw different equipment based on product name
    center_x, center_y = 300, 180
    
    if 'french press' in product_name.lower():
        # Draw a french press
        draw.rectangle((center_x-60, center_y-100, center_x+60, center_y+80), fill=(192, 192, 192))
        draw.rectangle((center_x-40, center_y-80, center_x+40, center_y+60), fill=(220, 220, 220))
        draw.line((center_x, center_y-120, center_x, center_y-80), fill=(192, 192, 192), width=10)
        draw.ellipse((center_x-15, center_y-140, center_x+15, center_y-110), fill=(192, 192, 192))
    
    elif 'cold brew' in product_name.lower():
        # Draw a cold brew container
        draw.rectangle((center_x-40, center_y-80, center_x+40, center_y+100), fill=(220, 220, 220))
        draw.line((center_x-40, center_y-80, center_x+40, center_y-80), fill=(192, 192, 192), width=5)
        draw.line((center_x-40, center_y+100, center_x+40, center_y+100), fill=(192, 192, 192), width=5)
        # Ice cubes
        for i in range(3):
            draw.rectangle((center_x-30+i*20, center_y-60+i*40, center_x-10+i*20, center_y-40+i*40), 
                           fill=(240, 240, 255))
    
    else:  # Pour over or default
        # Draw a pour over
        draw.polygon([(center_x-80, center_y+80), (center_x+80, center_y+80), 
                      (center_x+40, center_y-80), (center_x-40, center_y-80)], 
                    fill=(220, 220, 220))
        draw.ellipse((center_x-40, center_y-120, center_x+40, center_y-40), fill=(192, 192, 192))
    
    # Add product name
    try:
        # Try to use a default font
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
        draw.text((50, 320), product_name, fill=(255, 255, 255), font=font)
    except:
        # Fallback - no custom font
        draw.text((50, 320), product_name, fill=(255, 255, 255))
    
    # Save the image
    image_path = f'static/images/products/product_{product_id}.jpg'
    img.save(image_path)
    return image_path

# Create images for each product
for product in data['products']:
    product_id = product['id']
    product_name = product['name']
    category = product['category']
    
    if category == 'coffee':
        # Select a color based on roast level
        if 'dark' in product_name.lower() or 'espresso' in product_name.lower():
            color = (70, 40, 20)  # Dark roast
        elif 'light' in product_name.lower() or 'ethiopian' in product_name.lower():
            color = (160, 82, 45)  # Light roast
        else:
            color = (139, 69, 19)  # Medium roast
            
        image_path = create_coffee_image(product_id, product_name, color)
    else:
        image_path = create_equipment_image(product_id, product_name)
    
    # Update the product image path in the data
    product['image'] = f'/static/images/products/product_{product_id}.jpg'
    print(f"Created image for {product_name}")

# Also create a better hero image
def create_hero_image():
    img = Image.new('RGB', (800, 400), (100, 65, 23))
    draw = ImageDraw.Draw(img)
    
    # Draw a coffee shop scene
    # Background elements - coffee beans
    for i in range(20):
        x = i * 40 + 10
        y = 50 if i % 2 == 0 else 30
        draw.ellipse((x, y, x+20, y+30), fill=(80, 40, 20))
    
    # Coffee cup in center
    center_x, center_y = 400, 200
    draw.ellipse((center_x-80, center_y+20, center_x+80, center_y+100), fill=(230, 230, 230))
    draw.rectangle((center_x-80, center_y-80, center_x+80, center_y+60), fill=(230, 230, 230))
    draw.ellipse((center_x-60, center_y-110, center_x+60, center_y-50), fill=(200, 200, 200))
    
    # Coffee in cup
    draw.ellipse((center_x-60, center_y-90, center_x+60, center_y-70), fill=(120, 60, 20))
    
    # Steam
    for i in range(3):
        x_offset = i * 40 - 40
        draw.arc((center_x+x_offset, center_y-160, center_x+x_offset+80, center_y-110), 
                 start=180, end=0, fill=(255, 255, 255), width=5)
    
    # Save the image
    img.save('static/images/banners/hero.jpg')
    print("Created hero image")

create_hero_image()

# Save updated product data
with open('data/products.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Image generation complete!")