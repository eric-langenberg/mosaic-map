# tests/test_core.py
import pytest
from PIL import Image
import tempfile
import os
from mosaicmap import MosaicMap

@pytest.fixture
def sample_images():
    """Create temporary test images."""
    images = []
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create 3 test images of different sizes
        sizes = [(100, 100), (200, 150), (150, 200)]
        for i, size in enumerate(sizes):
            img = Image.new('RGB', size, (i * 50, i * 50, i * 50))
            path = os.path.join(tmpdir, f'test_{i}.png')
            img.save(path)
            images.append(path)
        yield images

def test_basic_creation(sample_images):
    treemap = MosaicMap()
    
    data = {
        'labels': ['A', 'B', 'C'],
        'values': [50, 30, 20],
        'image_paths': sample_images
    }
    
    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
        treemap.create(data, tmp.name)
        # Verify output image exists and can be opened
        img = Image.open(tmp.name)
        assert img.size == (800, 600)  # Default size

def test_invalid_mode():
    treemap = MosaicMap()
    with pytest.raises(ValueError):
        treemap.create({}, 'test.png', image_mode='invalid')

def test_missing_images(sample_images):
    treemap = MosaicMap()
    data = {
        'labels': ['A'],
        'values': [1],
        'image_paths': ['nonexistent.jpg']
    }
    with pytest.raises(FileNotFoundError):
        treemap.create(data, 'test.png')