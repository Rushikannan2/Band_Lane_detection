from django import forms


class DiseasePredictionForm(forms.Form):
    """
    Form for disease prediction with single gel image upload.
    """
    gel_image = forms.ImageField(
        label='Upload DNA Gel Image',
        help_text='Select a DNA gel electrophoresis image for disease prediction',
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
            'accept': 'image/*'
        })
    )


class ForensicsForm(forms.Form):
    """
    Form for forensics analysis with two gel images upload.
    """
    crime_scene_image = forms.ImageField(
        label='Crime Scene DNA Gel Image',
        help_text='Upload the DNA gel image from the crime scene',
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
            'accept': 'image/*'
        })
    )
    
    suspect_image = forms.ImageField(
        label='Suspect DNA Gel Image',
        help_text='Upload the DNA gel image from the suspect',
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
            'accept': 'image/*'
        })
    )
