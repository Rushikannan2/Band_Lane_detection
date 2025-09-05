#!/usr/bin/env python
"""
Test script for gel analysis functions.
This script tests the gel analysis module without Django dependencies.
"""

import os
import sys
import numpy as np
import cv2

# Add the gel_detection app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'gel_detection'))

# Set up Django environment
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        MEDIA_ROOT=os.path.join(os.path.dirname(__file__), 'media'),
        DEBUG=True
    )
    django.setup()

from gel_detection.gel_analysis import detect_bands, extract_features, visualize_detection, process_gel_image

def create_test_gel_image():
    """
    Create a synthetic gel electrophoresis image for testing.
    This creates a simple test image with simulated lanes and bands.
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

def test_gel_analysis():
    """
    Test the gel analysis functions with a synthetic image.
    """
    print("Creating synthetic gel electrophoresis image...")
    test_image = create_test_gel_image()
    
    # Save test image
    test_image_path = "test_gel.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"Test image saved as: {test_image_path}")
    
    print("\nTesting band detection...")
    lanes = detect_bands(test_image)
    print(f"Detected {len(lanes)} lanes")
    
    for i, lane in enumerate(lanes):
        print(f"  Lane {i+1}: {len(lane['bands'])} bands at positions {lane['bands']}")
    
    print("\nTesting feature extraction...")
    band_features, lane_features, image_features = extract_features(test_image, "test_gel.png")
    print(f"Extracted {len(band_features)} band features")
    print(f"Extracted {len(lane_features)} lane features")
    print(f"Image features: {image_features}")
    
    print("\nTesting visualization...")
    visualization = visualize_detection(test_image, lanes, "test_visualization.png")
    print("Visualization saved as: test_visualization.png")
    
    print("\nTesting complete processing pipeline...")
    # Set up minimal Django settings for testing
    import django
    from django.conf import settings
    
    if not settings.configured:
        settings.configure(
            MEDIA_ROOT=os.path.join(os.path.dirname(__file__), 'media'),
            DEBUG=True
        )
        django.setup()
    
    results = process_gel_image(test_image_path, "test_processed")
    print(f"Processing complete!")
    print(f"  Total bands: {results['total_bands']}")
    print(f"  Total lanes: {results['num_lanes']}")
    print(f"  Processed image: {results['processed_image_path']}")
    
    print("\n✅ All tests completed successfully!")
    
    # Clean up test files
    try:
        os.remove(test_image_path)
        os.remove("test_visualization.png")
        if os.path.exists(results['processed_image_path']):
            os.remove(results['processed_image_path'])
        print("Test files cleaned up.")
    except:
        pass

if __name__ == "__main__":
    test_gel_analysis()
