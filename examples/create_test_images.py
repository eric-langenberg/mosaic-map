# examples/create_test_images.py
from PIL import Image
import os

# Create directory for test images
os.makedirs('examples/test_images', exist_ok=True)

# Create some test images with different colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
sizes = [(100, 100), (200, 150), (150, 200)]

for i, (color, size) in enumerate(zip(colors, sizes)):
    img = Image.new('RGB', size, color)
    img.save(f'examples/test_images/image{i+1}.jpg')