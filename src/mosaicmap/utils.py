# src/mosaicmap/utils.py
from pathlib import Path
from typing import List, Union

def validate_image_paths(paths: List[Union[str, Path]]) -> List[Path]:
    """
    Validate that all provided paths exist and are image files.
    
    Args:
        paths: List of file paths to validate
        
    Returns:
        List of Path objects for valid images
        
    Raises:
        FileNotFoundError: If any path doesn't exist
        ValueError: If any file doesn't appear to be an image
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    validated_paths = []
    
    for path in paths:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        if path.suffix.lower() not in valid_extensions:
            raise ValueError(f"Unsupported file type: {path}")
        validated_paths.append(path)
    
    return validated_paths

def calculate_layout_dimensions(
    values: List[float],
    target_ratio: float = 1.0
) -> tuple:
    """
    Calculate optimal dimensions for the treemap layout.
    
    Args:
        values: List of numerical values
        target_ratio: Desired width/height ratio
        
    Returns:
        tuple: (width, height) in relative units
    """
    total = sum(values)
    area = 100  # Use 100 as base area
    
    # Calculate width and height maintaining target ratio
    height = (area / target_ratio) ** 0.5
    width = height * target_ratio
    
    return width, height