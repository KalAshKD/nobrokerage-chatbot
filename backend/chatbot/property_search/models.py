from django.db import models

class PropertyListing(models.Model):
    # Basic project info
    project_id = models.CharField(max_length=255, primary_key=True)
    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    possession_date = models.CharField(max_length=50, blank=True)
    project_summary = models.TextField(blank=True)
    slug = models.CharField(max_length=255, blank=True)
    
    # Location info
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=255)
    full_address = models.TextField(blank=True)
    landmark = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Property configuration
    bhk_type = models.CharField(max_length=50)
    property_category = models.CharField(max_length=100)
    
    # Pricing and details
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    carpet_area = models.FloatField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    balcony = models.IntegerField(null=True, blank=True)
    furnished_type = models.CharField(max_length=50, blank=True)
    
    # Images
    property_images = models.TextField(blank=True)  # Store as JSON string
    
    class Meta:
        db_table = 'property_listings'
    
    def __str__(self):
        return f"{self.project_name} - {self.bhk_type}"