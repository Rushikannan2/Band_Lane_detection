"""
Disease Pattern Recognition for Gel Electrophoresis

This module contains disease patterns and band signatures for common
genetic diseases that can be detected from gel electrophoresis patterns.
"""

# Disease patterns based on band characteristics
DISEASE_PATTERNS = {
    'sickle_cell_anemia': {
        'description': 'Sickle Cell Anemia',
        'band_count_range': (2, 3),
        'lane_count_range': (2, 4),
        'band_patterns': ['double_band', 'heterozygous'],
        'confidence_threshold': 0.8,
        'symptoms': ['Fatigue', 'Pain crises', 'Anemia']
    },
    'thalassemia': {
        'description': 'Thalassemia',
        'band_count_range': (1, 2),
        'lane_count_range': (2, 3),
        'band_patterns': ['single_band', 'reduced_hemoglobin'],
        'confidence_threshold': 0.7,
        'symptoms': ['Anemia', 'Fatigue', 'Weakness']
    },
    'cystic_fibrosis': {
        'description': 'Cystic Fibrosis',
        'band_count_range': (3, 5),
        'lane_count_range': (3, 6),
        'band_patterns': ['multiple_bands', 'complex_pattern'],
        'confidence_threshold': 0.75,
        'symptoms': ['Respiratory problems', 'Digestive issues', 'Salt imbalance']
    },
    'huntington_disease': {
        'description': 'Huntington Disease',
        'band_count_range': (2, 4),
        'lane_count_range': (2, 4),
        'band_patterns': ['trinucleotide_repeat', 'variable_bands'],
        'confidence_threshold': 0.8,
        'symptoms': ['Movement disorders', 'Cognitive decline', 'Psychiatric symptoms']
    },
    'muscular_dystrophy': {
        'description': 'Muscular Dystrophy',
        'band_count_range': (1, 3),
        'lane_count_range': (2, 4),
        'band_patterns': ['dystrophin_absence', 'muscle_protein'],
        'confidence_threshold': 0.7,
        'symptoms': ['Muscle weakness', 'Progressive disability', 'Cardiac issues']
    },
    'tay_sachs': {
        'description': 'Tay-Sachs Disease',
        'band_count_range': (1, 2),
        'lane_count_range': (2, 3),
        'band_patterns': ['enzyme_deficiency', 'lipid_metabolism'],
        'confidence_threshold': 0.8,
        'symptoms': ['Neurological deterioration', 'Vision loss', 'Seizures']
    },
    'normal': {
        'description': 'Normal (No Disease Detected)',
        'band_count_range': (0, 1),
        'lane_count_range': (1, 2),
        'band_patterns': ['normal_pattern'],
        'confidence_threshold': 0.9,
        'symptoms': ['No significant abnormalities']
    }
}

def analyze_disease_patterns(band_count, lane_count, band_positions=None, intensities=None):
    """
    Analyze gel electrophoresis patterns to predict specific diseases.
    
    Args:
        band_count (int): Total number of bands detected
        lane_count (int): Number of lanes detected
        band_positions (list): Y-positions of bands (optional)
        intensities (list): Band intensities (optional)
        
    Returns:
        dict: Disease prediction with confidence scores
    """
    predictions = []
    
    for disease, pattern in DISEASE_PATTERNS.items():
        # Check if band count matches pattern
        band_match = pattern['band_count_range'][0] <= band_count <= pattern['band_count_range'][1]
        
        # Check if lane count matches pattern
        lane_match = pattern['lane_count_range'][0] <= lane_count <= pattern['lane_count_range'][1]
        
        # Calculate confidence based on matches
        confidence = 0.0
        if band_match and lane_match:
            confidence = 0.8  # Base confidence for pattern match
        elif band_match or lane_match:
            confidence = 0.5  # Partial match
        else:
            confidence = 0.1  # Low confidence
        
        # Additional pattern analysis if positions provided
        if band_positions and len(band_positions) > 0:
            # Analyze band distribution patterns
            if len(band_positions) == 2 and abs(band_positions[0] - band_positions[1]) < 50:
                # Double band pattern (common in sickle cell)
                if disease == 'sickle_cell_anemia':
                    confidence += 0.2
            elif len(band_positions) >= 3:
                # Multiple bands (common in complex diseases)
                if disease in ['cystic_fibrosis', 'huntington_disease']:
                    confidence += 0.15
        
        # Check confidence threshold
        if confidence >= pattern['confidence_threshold']:
            predictions.append({
                'disease': disease,
                'description': pattern['description'],
                'confidence': min(confidence, 1.0),
                'symptoms': pattern['symptoms'],
                'pattern_match': {
                    'band_count': band_match,
                    'lane_count': lane_match
                }
            })
    
    # Sort by confidence
    predictions.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Return top prediction or normal if no matches
    if predictions and predictions[0]['confidence'] > 0.6:
        return predictions[0]
    else:
        return {
            'disease': 'normal',
            'description': 'Normal (No Disease Detected)',
            'confidence': 0.9,
            'symptoms': ['No significant abnormalities detected'],
            'pattern_match': {
                'band_count': True,
                'lane_count': True
            }
        }

def get_disease_recommendations(disease_prediction):
    """
    Get recommendations based on disease prediction.
    
    Args:
        disease_prediction (dict): Disease prediction result
        
    Returns:
        dict: Recommendations and next steps
    """
    disease = disease_prediction['disease']
    confidence = disease_prediction['confidence']
    
    recommendations = {
        'immediate_actions': [],
        'follow_up_tests': [],
        'consultation_required': False,
        'urgency_level': 'low'
    }
    
    if disease == 'normal':
        recommendations['immediate_actions'] = [
            'Continue regular health monitoring',
            'Maintain healthy lifestyle'
        ]
        recommendations['follow_up_tests'] = [
            'Annual genetic screening if family history exists'
        ]
    else:
        recommendations['consultation_required'] = True
        
        if confidence > 0.8:
            recommendations['urgency_level'] = 'high'
            recommendations['immediate_actions'] = [
                'Schedule immediate consultation with genetic counselor',
                'Inform primary care physician',
                'Consider family genetic testing'
            ]
        else:
            recommendations['urgency_level'] = 'medium'
            recommendations['immediate_actions'] = [
                'Schedule consultation with genetic counselor',
                'Discuss results with healthcare provider'
            ]
        
        # Disease-specific recommendations
        if disease == 'sickle_cell_anemia':
            recommendations['follow_up_tests'] = [
                'Hemoglobin electrophoresis',
                'Complete blood count',
                'Sickle cell solubility test'
            ]
        elif disease == 'cystic_fibrosis':
            recommendations['follow_up_tests'] = [
                'Sweat chloride test',
                'Genetic testing for CFTR mutations',
                'Pulmonary function tests'
            ]
        elif disease == 'huntington_disease':
            recommendations['follow_up_tests'] = [
                'Genetic testing for HTT gene',
                'Neurological examination',
                'MRI brain scan'
            ]
        else:
            recommendations['follow_up_tests'] = [
                'Comprehensive genetic panel',
                'Specialist consultation',
                'Family history analysis'
            ]
    
    return recommendations
