# src/mosaicmap/core.py
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import squarify
import pandas as pd
from pathlib import Path
from typing import Dict, List, Union, Literal

class MosaicMap:
    """
    A class to generate treemaps with images instead of plain rectangles.
    """
    
    def __init__(self):
        self.supported_modes = ['crop', 'stretch']
    
    def _validate_inputs(self, data: Dict) -> None:
        """Validate input data structure and contents."""
        required_keys = ['labels', 'values', 'image_paths']
        if not all(key in data for key in required_keys):
            raise ValueError(f"Data must contain all of: {required_keys}")
        
        if not (len(data['labels']) == len(data['values']) == len(data['image_paths'])):
            raise ValueError("All input lists must have the same length")
        
        # Validate image paths exist
        for path in data['image_paths']:
            if not Path(path).is_file():
                raise FileNotFoundError(f"Image not found: {path}")
    
    def _process_image(self, 
                      img: Image.Image, 
                      target_size: tuple, 
                      mode: Literal['crop', 'stretch']) -> Image.Image:
        """Process single image according to specified mode."""
        if mode == 'stretch':
            return img.resize(target_size, Image.Resampling.LANCZOS)
        
        elif mode == 'crop':
            # Calculate aspect ratios
            target_ratio = target_size[0] / target_size[1]
            img_ratio = img.width / img.height
            
            if img_ratio > target_ratio:
                # Image is wider than target
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img.height))
            else:
                # Image is taller than target
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                img = img.crop((0, top, img.width, top + new_height))
            
            return img.resize(target_size, Image.Resampling.LANCZOS)

    def _create_label_overlay(self, 
                            rect: dict,
                            label: str,
                            font: ImageFont.FreeTypeFont,
                            draw: ImageDraw.ImageDraw) -> tuple:
        """Create a label overlay with semi-transparent background."""
        # Get text size
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate position (centered horizontally, near top vertically)
        x = rect['x'] + (rect['dx'] - text_width) / 2
        y = rect['y'] + 10  # 10 pixels from top
        
        # Create padding around text
        padding = 4
        bg_bbox = (
            x - padding,
            y - padding,
            x + text_width + padding,
            y + text_height + padding
        )
        
        # Draw semi-transparent black background
        draw.rectangle(bg_bbox, fill=(0, 0, 0, 128))  # 128 is 50% opacity
        
        return (x, y)
    
    def create(self,
               data: Dict[str, List],
               output_path: str,
               image_mode: Literal['crop', 'stretch'] = 'crop',
               width: int = 800,
               height: int = 600,
               background_color: tuple = (255, 255, 255),
               show_labels: bool = False,
               font_size: int = 14) -> None:
        """
        Create an image treemap from the provided data.
        
        Args:
            data: Dictionary containing 'labels', 'values', and 'image_paths'
            output_path: Path where the output image will be saved
            image_mode: How to handle image aspect ratios ('crop' or 'stretch')
            width: Width of output image in pixels
            height: Height of output image in pixels
            background_color: RGB tuple for background color
            show_labels: Whether to show labels on the images
            font_size: Font size for labels (if shown)
        """
        if image_mode not in self.supported_modes:
            raise ValueError(f"Mode must be one of: {self.supported_modes}")
        
        self._validate_inputs(data)
        
        # Calculate treemap layout
        normed = squarify.normalize_sizes(data['values'], dx=width, dy=height)
        rects = squarify.squarify(normed, 0, 0, width, height)
        
        # Create base image
        base_img = Image.new('RGB', (width, height), background_color)
        
        # Create a single transparent overlay for all labels if needed
        if show_labels:
            label_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(label_overlay)
            # Try to load a system font, fall back to default if not found
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()
        
        # Process each rectangle
        for rect, img_path, label in zip(rects, data['image_paths'], data['labels']):
            # Load and process image
            with Image.open(img_path) as img:
                rect_width = int(rect['dx'])
                rect_height = int(rect['dy'])
                processed_img = self._process_image(
                    img.convert('RGB'),
                    (rect_width, rect_height),
                    image_mode
                )
                
                # Paste onto base image
                base_img.paste(
                    processed_img,
                    (int(rect['x']), int(rect['y']))
                )
        
        # Add all labels after images are placed
        if show_labels:
            # Create all labels on the overlay
            for rect, label in zip(rects, data['labels']):
                text_pos = self._create_label_overlay(rect, label, font, overlay_draw)
                overlay_draw.text(text_pos, label, fill=(255, 255, 255), font=font)
            
            # Composite the label overlay onto the base image
            base_img = Image.alpha_composite(base_img.convert('RGBA'), label_overlay).convert('RGB')
        
        # Save result
        base_img.save(output_path, quality=95)