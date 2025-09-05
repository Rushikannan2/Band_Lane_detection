#!/usr/bin/env python
"""
Create a test gel electrophoresis image for testing the Django application.
"""

import cv2
import numpy as np
import os

def create_test_gel_image():
    """
    Create a synthetic gel electrophoresis image for testing.
    """
    # Create a 400x300 grayscale image (height x width)
    image = np.ones((400, 300), dtype=np.uint8) * 240  # Light gray background
    
    # Add some noise
    noise = np.random.normal(0, 10, image.shape).astype(np.uint8)
    image = np.clip(image + noise, 0, 255)
    
    # Create 3 lanes (vertical columns)
    lane_positions = [75, 150, 225]
    lane_width = 20
    
    for i, lane_x in enumerate(lane_positions):
        # Create lane background (slightly darker)
        image[:, lane_x-lane_width//2:lane_x+lane_width//2] = 200
        
        # Add bands (horizontal dark lines)
        if i == 0:  # Lane 1: 2 bands
            band_positions = [100, 200]
        elif i == 1:  # Lane 2: 3 bands
            band_positions = [80, 150, 250]
        else:  # Lane 3: 1 band
            band_positions = [120]
        
        for band_y in band_positions:
            # Create band (dark horizontal line)
            band_height = 8
            start_y = max(0, band_y - band_height//2)
            end_y = min(image.shape[0], band_y + band_height//2)
            image[start_y:end_y, lane_x-lane_width//2:lane_x+lane_width//2] = 50
    
    return image

if __name__ == "__main__":
    print("Creating test gel electrophoresis image...")
    test_image = create_test_gel_image()
    
    # Save test image
    test_image_path = "test_gel_sample.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"Test image saved as: {test_image_path}")
    print("You can now upload this image to test the Django application!")
    print("The image contains 3 lanes with 2, 3, and 1 bands respectively.")
