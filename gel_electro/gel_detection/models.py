from django.db import models


class GelImage(models.Model):
    """
    Model to store information about uploaded gel images.
    This is optional as per requirements but useful for tracking uploads.
    """
    # Original uploaded image
    original_image = models.ImageField(upload_to='uploads/')
    # Processed image with band detection overlay
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)
    # Number of bands detected
    band_count = models.IntegerField(default=0)
    # Timestamp of upload
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Gel Image {self.id} - {self.band_count} bands detected"
