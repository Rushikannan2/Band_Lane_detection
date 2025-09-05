#!/usr/bin/env python
"""
Create a better test gel electrophoresis image for testing the Django application.
This creates a more realistic gel image with clear bands that should be detected.
"""

import cv2
import numpy as np
import os

def create_realistic_gel_image():
    """
    Create a more realistic gel electrophoresis image for testing.
    """
    # Create a 400x300 grayscale image (height x width)
    image = np.ones((400, 300), dtype=np.uint8) * 240  # Light gray background
    
    # Add some noise
    noise = np.random.normal(0, 5, image.shape).astype(np.uint8)
    image = np.clip(image + noise, 0, 255)
    
    # Create 4 lanes (vertical columns)
    lane_positions = [60, 120, 180, 240]
    lane_width = 25
    
    for i, lane_x in enumerate(lane_positions):
        # Create lane background (slightly darker)
        image[:, lane_x-lane_width//2:lane_x+lane_width//2] = 200
        
        # Add bands (horizontal dark lines) - make them more prominent
        if i == 0:  # Lane 1: 3 bands
            band_positions = [80, 150, 220]
        elif i == 1:  # Lane 2: 2 bands
            band_positions = [100, 180]
        elif i == 2:  # Lane 3: 4 bands
            band_positions = [70, 120, 170, 250]
        else:  # Lane 4: 1 band
            band_positions = [140]
        
        for band_y in band_positions:
            # Create band (dark horizontal line) - make it thicker and darker
            band_height = 12
            start_y = max(0, band_y - band_height//2)
            end_y = min(image.shape[0], band_y + band_height//2)
            # Make bands darker and more prominent
            image[start_y:end_y, lane_x-lane_width//2:lane_x+lane_width//2] = 30
    
    # Add some additional noise to make it more realistic
    noise2 = np.random.normal(0, 3, image.shape).astype(np.uint8)
    image = np.clip(image + noise2, 0, 255)
    
    return image

if __name__ == "__main__":
    print("Creating realistic test gel electrophoresis image...")
    test_image = create_realistic_gel_image()
    
    # Save test image
    test_image_path = "realistic_test_gel.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"Realistic test image saved as: {test_image_path}")
    print("This image has 4 lanes with 3, 2, 4, and 1 bands respectively.")
    print("The bands are darker and more prominent for better detection.")
