"""
Advanced Gel Electrophoresis Band Detection using OpenCV Contours

This module provides more robust band detection using contour analysis
instead of just peak finding, which should work better with real gel images.
"""

import cv2
import numpy as np
from scipy.signal import find_peaks


def detect_bands_advanced(image, min_band_area=50, max_band_area=5000):
    """
    Advanced band detection using contour analysis and morphological operations.
    
    This function uses a more robust approach:
    1. Preprocessing with noise reduction
    2. Edge detection and contour finding
    3. Filtering contours based on shape and size
    4. Grouping bands by vertical position (lanes)
    
    Args:
        image (numpy.ndarray): Grayscale gel electrophoresis image
        min_band_area (int): Minimum area for a valid band contour
        max_band_area (int): Maximum area for a valid band contour
        
    Returns:
        list: List of dictionaries containing lane information
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to create binary image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Invert so bands become white objects
    inverted = cv2.bitwise_not(thresh)
    
    # Apply morphological operations to clean up the image
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area and aspect ratio
    valid_bands = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_band_area < area < max_band_area:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            # Bands should be wider than they are tall (horizontal rectangles)
            if aspect_ratio > 1.5 and w > 20:
                # Calculate center point
                center_x = x + w // 2
                center_y = y + h // 2
                
                valid_bands.append({
                    'contour': contour,
                    'center_x': center_x,
                    'center_y': center_y,
                    'area': area,
                    'width': w,
                    'height': h,
                    'bbox': (x, y, w, h)
                })
    
    # Group bands by vertical position (lanes)
    lanes = group_bands_into_lanes(valid_bands, image.shape[1])
    
    return lanes


def group_bands_into_lanes(bands, image_width, lane_tolerance=50):
    """
    Group detected bands into lanes based on their horizontal position.
    
    Args:
        bands (list): List of band dictionaries
        image_width (int): Width of the image
        lane_tolerance (int): Maximum horizontal distance to consider bands in same lane
        
    Returns:
        list: List of lane dictionaries
    """
    if not bands:
        # If no bands detected, create default lanes
        num_default_lanes = max(1, image_width // 100)
        lanes = []
        for i in range(num_default_lanes):
            lane_x = (i + 1) * image_width // (num_default_lanes + 1)
            lanes.append({
                'lane_index': i + 1,
                'lane_x': lane_x,
                'bands': [],
                'intensities': [],
                'sharpness': 0
            })
        return lanes
    
    # Sort bands by horizontal position
    bands.sort(key=lambda b: b['center_x'])
    
    # Group bands into lanes
    lanes = []
    current_lane = []
    current_lane_x = bands[0]['center_x']
    
    for band in bands:
        if abs(band['center_x'] - current_lane_x) <= lane_tolerance:
            current_lane.append(band)
        else:
            # Start new lane
            if current_lane:
                lanes.append(create_lane_from_bands(current_lane, len(lanes) + 1))
            current_lane = [band]
            current_lane_x = band['center_x']
    
    # Add the last lane
    if current_lane:
        lanes.append(create_lane_from_bands(current_lane, len(lanes) + 1))
    
    return lanes


def create_lane_from_bands(bands, lane_index):
    """
    Create a lane dictionary from a list of bands.
    
    Args:
        bands (list): List of band dictionaries
        lane_index (int): Lane number
        
    Returns:
        dict: Lane dictionary
    """
    if not bands:
        return {
            'lane_index': lane_index,
            'lane_x': 0,
            'bands': [],
            'intensities': [],
            'sharpness': 0
        }
    
    # Calculate average lane position
    lane_x = int(np.mean([band['center_x'] for band in bands]))
    
    # Extract band positions and intensities
    band_positions = [band['center_y'] for band in bands]
    band_intensities = [band['area'] for band in bands]  # Use area as intensity proxy
    
    # Calculate average sharpness (using area as proxy)
    sharpness = float(np.mean(band_intensities)) if band_intensities else 0
    
    return {
        'lane_index': lane_index,
        'lane_x': lane_x,
        'bands': np.array(band_positions),
        'intensities': np.array(band_intensities),
        'sharpness': sharpness
    }


def detect_bands_hybrid(image, lane_distance=30, min_distance=10, prominence=0.1):
    """
    Hybrid band detection combining contour analysis and peak finding.
    
    This function tries multiple detection methods and returns the best result.
    
    Args:
        image (numpy.ndarray): Grayscale gel electrophoresis image
        lane_distance (int): Minimum distance between detected lanes
        min_distance (int): Minimum distance between detected bands
        prominence (float): Minimum prominence for band detection
        
    Returns:
        list: List of dictionaries containing lane information
    """
    # Try advanced contour-based detection first
    contour_lanes = detect_bands_advanced(image)
    
    # Count total bands from contour detection
    total_contour_bands = sum(len(lane['bands']) for lane in contour_lanes)
    
    # If contour detection found bands, use it
    if total_contour_bands > 0:
        return contour_lanes
    
    # Otherwise, fall back to original peak-finding method
    return detect_bands_original(image, lane_distance, min_distance, prominence)


def detect_bands_original(image, lane_distance=30, min_distance=10, prominence=0.1):
    """
    Original peak-finding based band detection (fallback method).
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to enhance bands
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Invert image for better peak detection (dark bands become bright peaks)
    inv = cv2.bitwise_not(thresh)

    # Detect lanes using vertical projection profile
    lane_profile = np.sum(inv, axis=0)
    if np.max(lane_profile) > 0:
        lane_profile = lane_profile / np.max(lane_profile)
    else:
        lane_profile = np.zeros_like(lane_profile)

    # Find peaks in vertical projection to identify lane centers
    lane_peaks, _ = find_peaks(lane_profile, distance=lane_distance, prominence=0.1, height=0.3)

    # If no lanes detected, try with even lower parameters
    if len(lane_peaks) == 0:
        lane_peaks, _ = find_peaks(lane_profile, distance=20, prominence=0.05, height=0.2)
    
    # If still no lanes, create default lanes based on image width
    if len(lane_peaks) == 0:
        width = image.shape[1]
        num_lanes = max(1, width // 100)  # Estimate lanes based on width
        lane_peaks = np.linspace(width // (num_lanes + 1), width - width // (num_lanes + 1), num_lanes).astype(int)

    lane_results = []
    
    # Process each detected lane
    for lane_idx, lane_x in enumerate(lane_peaks, start=1):
        # Extract lane region (wider region for better band detection)
        lane_width = 15
        lane = inv[:, max(0, lane_x-lane_width//2):min(inv.shape[1], lane_x+lane_width//2)]

        # Create horizontal projection profile for this lane
        lane_profile = np.sum(lane, axis=1)
        if np.max(lane_profile) > 0:
            lane_profile = lane_profile / np.max(lane_profile)
        else:
            lane_profile = np.zeros_like(lane_profile)

        # Detect bands as peaks in horizontal projection
        bands, props = find_peaks(lane_profile, distance=min_distance, prominence=prominence, height=0.2)

        # If no bands detected, try with even lower parameters
        if len(bands) == 0:
            bands, props = find_peaks(lane_profile, distance=5, prominence=0.05, height=0.1)

        # Calculate average sharpness of detected bands
        sharpness = float(np.mean(props["prominences"])) if len(bands) > 0 and "prominences" in props else 0

        lane_results.append({
            "lane_index": lane_idx,
            "lane_x": int(lane_x),
            "bands": bands,
            "intensities": lane_profile[bands] if len(bands) > 0 else np.array([]),
            "sharpness": sharpness
        })

    return lane_results
