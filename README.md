# MosaicMap

A Python library for creating treemaps where rectangles are replaced with images. Perfect for visualizing comparisons and part-to-whole relationships with striking visuals.

## Installation

```bash
pip install mosaicmap
```

## Features

- Create treemaps using local images
- Two image fitting modes: 'crop' and 'stretch'
- Simple and intuitive API
- Customizable output size, background color, and labels

## Example Ouptut
This example shows cities sized by time spent:

![Example Output](resources/example_output.jpg)

## Usage

```python
from mosaicmap import MosaicMap

# Initialize mosaicmap creator
mosaicmap = MosaicMap()

# Prepare your data
data = {
    'labels': ['Product A', 'Product B', 'Product C'],
    'values': [500, 300, 200],  # Size values for each rectangle
    'image_paths': ['path/to/image1.jpg', 'path/to/image2.jpg', 'path/to/image3.jpg']
}

# Create the mosaicmap
mosaicmap.create(
    data=data,
    output_path='output_mosaicmap.png',
    image_mode='crop',  # or 'stretch'
    width=800,
    height=600,
    background_color=(255, 255, 255),  # white
    show_labels=True,  # Enable labels, False by default
    font_size=16  # Optionally adjust font size
)
```

## Image Modes

- **crop**: Maintains image aspect ratio by cropping excess portions
- **stretch**: Stretches or compresses images to fit exactly in their allocated rectangles

## Requirements

- Python 3.7+
- Pillow
- numpy
- squarify
- pandas

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
