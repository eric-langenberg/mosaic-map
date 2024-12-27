from mosaicmap import MosaicMap

# Create sample data
data = {
    'labels': ['A', 'B', 'C'],
    'values': [50, 30, 20],
    'image_paths': [
        'examples/test_images/image1.jpg',
        'examples/test_images/image2.jpg',
        'examples/test_images/image3.jpg'
    ]
}

# Create mosaic map
mosaic = MosaicMap()
mosaic.create(data, 'examples/test_output.jpg', show_labels=True, font_size=20)