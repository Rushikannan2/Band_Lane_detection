import os
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import DiseasePredictionForm, ForensicsForm
from .models import GelImage
from .gel_analysis import process_gel_image as analyze_gel_image, compare_gel_images
from .disease_patterns import analyze_disease_patterns, get_disease_recommendations


def home(request):
    """
    Homepage view displaying basic information about the project.
    """
    return render(request, 'home.html')


def about_author(request):
    """
    About Author page view displaying information about VT Rushi Kannan.
    """
    return render(request, 'about_author.html')


def faqs(request):
    """
    FAQs page view displaying frequently asked questions.
    """
    return render(request, 'faqs.html')


def process_gel_image(image_file):
    """
    Process a gel electrophoresis image using the advanced analysis module.
    
    This function handles the Django file upload and calls the gel analysis
    functions to detect lanes and bands with high accuracy.
    
    Args:
        image_file: Django uploaded file object
        
    Returns:
        tuple: (band_count, processed_image_path, original_image_path, analysis_results)
    """
    # Generate unique filenames
    unique_id = str(uuid.uuid4())
    original_filename = f"original_{unique_id}.png"
    
    # Save original image
    original_path = os.path.join(settings.MEDIA_ROOT, 'uploads', original_filename)
    os.makedirs(os.path.dirname(original_path), exist_ok=True)
    
    with open(original_path, 'wb') as f:
        for chunk in image_file.chunks():
            f.write(chunk)
    
    # Process the image using the advanced analysis module
    analysis_results = analyze_gel_image(original_path, f"processed_{unique_id}")
    
    # Extract processed image path (relative to media root)
    processed_relative_path = os.path.relpath(analysis_results['processed_image_path'], settings.MEDIA_ROOT)
    processed_filename = os.path.basename(processed_relative_path)
    
    return (
        analysis_results['total_bands'], 
        processed_filename, 
        original_filename,
        analysis_results
    )


def disease_prediction(request):
    """
    Handle disease prediction form submission.
    Processes single gel image using advanced analysis and returns prediction results.
    """
    if request.method == 'POST':
        form = DiseasePredictionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Process the uploaded image using advanced analysis
                band_count, processed_filename, original_filename, analysis_results = process_gel_image(
                    form.cleaned_data['gel_image']
                )
                
                # Enhanced prediction based on lane and band analysis
                num_lanes = analysis_results['num_lanes']
                total_bands = analysis_results['total_bands']
                
                # Extract band positions and intensities for pattern analysis
                band_positions = []
                band_intensities = []
                for lane in analysis_results['lanes']:
                    band_positions.extend(lane['bands'].tolist() if hasattr(lane['bands'], 'tolist') else lane['bands'])
                    band_intensities.extend(lane['intensities'].tolist() if hasattr(lane['intensities'], 'tolist') else lane['intensities'])
                
                # Use advanced disease pattern recognition
                disease_prediction = analyze_disease_patterns(
                    total_bands, num_lanes, band_positions, band_intensities
                )
                
                # Get recommendations
                recommendations = get_disease_recommendations(disease_prediction)
                
                # Format prediction results
                prediction = f"Disease: {disease_prediction['description']}"
                confidence = f"{disease_prediction['confidence']:.1%}"
                
                # Save to database with enhanced metadata (optional)
                try:
                    gel_image = GelImage.objects.create(
                        original_image=f'uploads/{original_filename}',
                        processed_image=f'processed/{processed_filename}',
                        band_count=total_bands
                    )
                except Exception as db_error:
                    print(f"Database save failed (continuing anyway): {db_error}")
                
                context = {
                    'prediction': prediction,
                    'confidence': confidence,
                    'band_count': total_bands,
                    'lane_count': num_lanes,
                    'original_image': f'/media/uploads/{original_filename}',
                    'processed_image': f'/media/processed/{processed_filename}',
                    'disease_info': {
                        'name': disease_prediction['description'],
                        'confidence_score': disease_prediction['confidence'],
                        'symptoms': disease_prediction['symptoms'],
                        'pattern_match': disease_prediction['pattern_match']
                    },
                    'recommendations': recommendations,
                    'analysis_details': {
                        'lanes_detected': num_lanes,
                        'bands_per_lane': total_bands / num_lanes if num_lanes > 0 else 0,
                        'image_quality': 'Good' if analysis_results['features']['image']['edge_mean'] > 0.1 else 'Fair'
                    }
                }
                return render(request, 'disease_result.html', context)
                
            except Exception as e:
                # Add debug information
                print(f"Error processing image: {str(e)}")
                import traceback
                traceback.print_exc()
                form.add_error('gel_image', f'Error processing image: {str(e)}')
        else:
            # Add debug information for form validation errors
            print(f"Form validation errors: {form.errors}")
    else:
        form = DiseasePredictionForm()
    
    return render(request, 'disease_prediction.html', {'disease_form': form})


def forensics_analysis(request):
    """
    Handle forensics analysis form submission.
    Processes two gel images using advanced analysis and computes match score.
    """
    if request.method == 'POST':
        form = ForensicsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save uploaded images first
                unique_id1 = str(uuid.uuid4())
                unique_id2 = str(uuid.uuid4())
                
                crime_original_filename = f"crime_{unique_id1}.png"
                suspect_original_filename = f"suspect_{unique_id2}.png"
                
                # Save crime scene image
                crime_path = os.path.join(settings.MEDIA_ROOT, 'uploads', crime_original_filename)
                os.makedirs(os.path.dirname(crime_path), exist_ok=True)
                with open(crime_path, 'wb') as f:
                    for chunk in form.cleaned_data['crime_scene_image'].chunks():
                        f.write(chunk)
                
                # Save suspect image
                suspect_path = os.path.join(settings.MEDIA_ROOT, 'uploads', suspect_original_filename)
                with open(suspect_path, 'wb') as f:
                    for chunk in form.cleaned_data['suspect_image'].chunks():
                        f.write(chunk)
                
                # Use advanced comparison analysis
                comparison_results = compare_gel_images(
                    crime_path, 
                    suspect_path,
                    f"crime_processed_{unique_id1}",
                    f"suspect_processed_{unique_id2}"
                )
                
                # Extract results
                crime_results = comparison_results['image1_results']
                suspect_results = comparison_results['image2_results']
                match_score = comparison_results['match_score']
                comparison_details = comparison_results['comparison_details']
                
                # Save both images to database (optional)
                try:
                    crime_gel = GelImage.objects.create(
                        original_image=f'uploads/{crime_original_filename}',
                        processed_image=f'processed/{os.path.basename(crime_results["processed_image_path"])}',
                        band_count=crime_results['total_bands']
                    )
                    suspect_gel = GelImage.objects.create(
                        original_image=f'uploads/{suspect_original_filename}',
                        processed_image=f'processed/{os.path.basename(suspect_results["processed_image_path"])}',
                        band_count=suspect_results['total_bands']
                    )
                except Exception as db_error:
                    print(f"Database save failed (continuing anyway): {db_error}")
                
                context = {
                    'match_score': match_score,
                    'crime_bands': crime_results['total_bands'],
                    'suspect_bands': suspect_results['total_bands'],
                    'crime_lanes': crime_results['num_lanes'],
                    'suspect_lanes': suspect_results['num_lanes'],
                    'crime_original': f'/media/uploads/{crime_original_filename}',
                    'crime_processed': f'/media/processed/{os.path.basename(crime_results["processed_image_path"])}',
                    'suspect_original': f'/media/uploads/{suspect_original_filename}',
                    'suspect_processed': f'/media/processed/{os.path.basename(suspect_results["processed_image_path"])}',
                    'comparison_details': comparison_details,
                    'analysis_quality': {
                        'crime_quality': 'Good' if crime_results['features']['image']['edge_mean'] > 0.1 else 'Fair',
                        'suspect_quality': 'Good' if suspect_results['features']['image']['edge_mean'] > 0.1 else 'Fair'
                    }
                }
                return render(request, 'forensics_result.html', context)
                
            except Exception as e:
                # Add debug information
                print(f"Error processing images: {str(e)}")
                import traceback
                traceback.print_exc()
                form.add_error(None, f'Error processing images: {str(e)}')
        else:
            # Add debug information for form validation errors
            print(f"Forensics form validation errors: {form.errors}")
    else:
        form = ForensicsForm()
    
    return render(request, 'forecast_analysis.html', {'forensics_form': form})


