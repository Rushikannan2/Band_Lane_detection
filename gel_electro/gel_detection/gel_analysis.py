"""
Gel Electrophoresis Analysis Module for Django

This module provides functions for analyzing DNA gel electrophoresis images
without augmentation. Functions are designed to be called from Django views
to process user-uploaded images.

Author: Django Gel Detection App
"""

import os
import cv2
import numpy as np
from scipy.signal import find_peaks
from django.conf import settings
from .advanced_detection import detect_bands_hybrid


def detect_bands(image, lane_distance=30, min_distance=10, prominence=0.1):
    """
    Detect DNA bands using hybrid approach (contour analysis + peak finding).
    
    This function uses the most robust detection method available:
    1. First tries advanced contour-based detection
    2. Falls back to peak-finding if contour detection fails
    
    Args:
        image (numpy.ndarray): Grayscale gel electrophoresis image
        lane_distance (int): Minimum distance between detected lanes
        min_distance (int): Minimum distance between detected bands
        prominence (float): Minimum prominence for band detection
        
    Returns:
        list: List of dictionaries containing lane information:
            - lane_index: Sequential lane number
            - lane_x: X-coordinate of lane center
            - bands: Array of Y-coordinates where bands are detected
            - intensities: Array of band intensities
            - sharpness: Average sharpness of bands in this lane
    """
    return detect_bands_hybrid(image, lane_distance, min_distance, prominence)


def extract_features(image, filename):
    """
    Extract comprehensive features from a gel electrophoresis image.
    
    This function analyzes the image at three levels:
    - Band-level: Individual DNA band characteristics
    - Lane-level: Characteristics of each lane (sample)
    - Image-level: Overall image characteristics
    
    Args:
        image (numpy.ndarray): Grayscale gel electrophoresis image
        filename (str): Original filename of the image
        
    Returns:
        tuple: (band_rows, lane_rows, image_row)
            - band_rows: List of dictionaries with band-level features
            - lane_rows: List of dictionaries with lane-level features  
            - image_row: Dictionary with image-level features
    """
    band_rows = []
    lane_rows = []
    
    # Detect lanes and bands in the image
    lanes = detect_bands(image)

    # Calculate global image statistics
    mean_intensity = float(np.mean(image))
    std_intensity = float(np.std(image))
    
    # Edge detection for image quality assessment
    edges = cv2.Canny(image, 50, 150)
    edge_sum = float(np.sum(edges))
    edge_mean = float(np.mean(edges))

    total_bands = 0

    # Process each detected lane
    for lane in lanes:
        total_bands += len(lane["bands"])

        # Create lane-level feature row
        lane_rows.append({
            "filename": filename,
            "lane_index": lane["lane_index"],
            "lane_x": lane["lane_x"],
            "num_bands": len(lane["bands"]),
            "avg_band_sharpness": lane["sharpness"],
            "mean_intensity": mean_intensity,
            "std_intensity": std_intensity,
            "edge_sum": edge_sum,
            "edge_mean": edge_mean,
        })

        # Create band-level feature rows for each band in this lane
        for band_idx, (pos, intensity) in enumerate(zip(lane["bands"], lane["intensities"]), start=1):
            band_id = f"{os.path.splitext(filename)[0]}_lane{lane['lane_index']}_band{band_idx}"
            band_rows.append({
                "band_id": band_id,
                "filename": filename,
                "lane_index": lane["lane_index"],
                "lane_x": lane["lane_x"],
                "band_index": band_idx,
                "band_position": int(pos),
                "band_intensity": float(intensity),
                "band_sharpness": lane["sharpness"],
                "mean_intensity": mean_intensity,
                "std_intensity": std_intensity,
                "edge_sum": edge_sum,
                "edge_mean": edge_mean,
            })

    # Create image-level feature row
    image_row = {
        "filename": filename,
        "num_lanes": len(lanes),
        "total_bands": total_bands,
        "mean_intensity": mean_intensity,
        "std_intensity": std_intensity,
        "edge_sum": edge_sum,
        "edge_mean": edge_mean,
    }

    return band_rows, lane_rows, image_row


def visualize_detection(image, lanes, save_path=None):
    """
    Create a visualization of detected lanes and bands.
    
    This function draws colored overlays on the original image showing:
    - Green vertical lines for detected lanes
    - Red horizontal lines for detected bands
    
    Args:
        image (numpy.ndarray): Original grayscale image
        lanes (list): List of lane dictionaries from detect_bands()
        save_path (str, optional): Path to save the visualization image
        
    Returns:
        numpy.ndarray: Image with detection overlays (BGR format)
    """
    # Convert grayscale to BGR for colored overlays
    if len(image.shape) == 2:
        img_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        img_rgb = image.copy()
    
    # Draw lane markers (green vertical lines)
    for lane in lanes:
        x = lane['lane_x']
        # Draw thicker lane markers
        cv2.line(img_rgb, (x, 0), (x, image.shape[0]), (0, 255, 0), 3)
        
        # Draw band markers (red horizontal lines)
        for i, y in enumerate(lane['bands']):
            # Draw thicker band markers
            cv2.line(img_rgb, (x-15, y), (x+15, y), (0, 0, 255), 3)
            # Add band number label
            cv2.putText(img_rgb, f'B{i+1}', (x+20, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # Add lane numbers
    for i, lane in enumerate(lanes):
        x = lane['lane_x']
        cv2.putText(img_rgb, f'L{i+1}', (x-10, 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Save visualization if path provided
    if save_path:
        cv2.imwrite(save_path, img_rgb)
    
    return img_rgb


def process_gel_image(image_path, output_filename=None):
    """
    Complete gel electrophoresis image processing pipeline.
    
    This is the main function that processes a single gel image through the
    entire analysis pipeline: band detection, feature extraction, and visualization.
    
    Args:
        image_path (str): Path to the input gel image
        output_filename (str, optional): Base filename for output files
        
    Returns:
        dict: Analysis results containing:
            - num_lanes: Number of detected lanes
            - total_bands: Total number of detected bands
            - lanes: List of lane information
            - features: Extracted features (band, lane, image level)
            - processed_image_path: Path to saved visualization
            - original_image_path: Path to original image
    """
    # Generate output filename if not provided
    if not output_filename:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_filename = base_name
    
    # Read and convert image to grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    # Detect lanes and bands
    lanes = detect_bands(image)
    
    # Extract features
    band_features, lane_features, image_features = extract_features(image, os.path.basename(image_path))
    
    # Create visualization
    processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed', f"{output_filename}_processed.png")
    os.makedirs(os.path.dirname(processed_image_path), exist_ok=True)
    
    visualize_detection(image, lanes, processed_image_path)
    
    # Calculate summary statistics
    total_bands = sum(len(lane['bands']) for lane in lanes)
    
    return {
        'num_lanes': len(lanes),
        'total_bands': total_bands,
        'lanes': lanes,
        'features': {
            'bands': band_features,
            'lanes': lane_features,
            'image': image_features
        },
        'processed_image_path': processed_image_path,
        'original_image_path': image_path
    }


def compare_gel_images(image1_path, image2_path, output_filename1=None, output_filename2=None):
    """
    Compare two gel electrophoresis images for forensics analysis.
    
    This function processes two images and calculates a similarity score
    based on band patterns and lane characteristics.
    
    Args:
        image1_path (str): Path to first gel image (e.g., crime scene)
        image2_path (str): Path to second gel image (e.g., suspect)
        output_filename1 (str, optional): Base filename for first image outputs
        output_filename2 (str, optional): Base filename for second image outputs
        
    Returns:
        dict: Comparison results containing:
            - image1_results: Analysis results for first image
            - image2_results: Analysis results for second image
            - match_score: Similarity score (0-100)
            - comparison_details: Detailed comparison metrics
    """
    # Process both images
    results1 = process_gel_image(image1_path, output_filename1)
    results2 = process_gel_image(image2_path, output_filename2)
    
    # Calculate match score based on lane and band characteristics
    match_score = calculate_match_score(results1, results2)
    
    # Detailed comparison metrics
    comparison_details = {
        'lane_count_diff': abs(results1['num_lanes'] - results2['num_lanes']),
        'band_count_diff': abs(results1['total_bands'] - results2['total_bands']),
        'lane_similarity': 1 - abs(results1['num_lanes'] - results2['num_lanes']) / max(results1['num_lanes'], results2['num_lanes'], 1),
        'band_similarity': 1 - abs(results1['total_bands'] - results2['total_bands']) / max(results1['total_bands'], results2['total_bands'], 1)
    }
    
    return {
        'image1_results': results1,
        'image2_results': results2,
        'match_score': match_score,
        'comparison_details': comparison_details
    }


def calculate_match_score(results1, results2):
    """
    Calculate similarity score between two gel analysis results.
    
    This function implements a heuristic algorithm to compare gel patterns
    based on lane count, band count, and relative positions.
    
    Args:
        results1 (dict): Analysis results from first image
        results2 (dict): Analysis results from second image
        
    Returns:
        float: Match score between 0 and 100
    """
    # Lane count similarity
    lane_similarity = 1 - abs(results1['num_lanes'] - results2['num_lanes']) / max(results1['num_lanes'], results2['num_lanes'], 1)
    
    # Band count similarity  
    band_similarity = 1 - abs(results1['total_bands'] - results2['total_bands']) / max(results1['total_bands'], results2['total_bands'], 1)
    
    # Position similarity (simplified - based on band count difference)
    position_similarity = max(0, 1 - abs(results1['total_bands'] - results2['total_bands']) * 0.1)
    
    # Combined score with weights: 60% band count, 40% position
    combined_score = (0.6 * band_similarity + 0.4 * position_similarity) * 100
    
    # Ensure score is between 0 and 100
    return max(0, min(100, combined_score))
