from django.core.management.base import BaseCommand
from property_search.models import PropertyListing

class Command(BaseCommand):
    help = 'Load emergency sample data for testing'
    
    def handle(self, *args, **options):
        # Clear existing data
        PropertyListing.objects.all().delete()
        
        # Create realistic sample data based on your CSV structure
        sample_properties = [
            {
                'project_id': 'sample_1',
                'project_name': 'Ashwini',
                'project_type': 'RESIDENTIAL',
                'status': 'UNDER_CONSTRUCTION',
                'city': 'Mumbai',
                'locality': 'Chembur',
                'bhk_type': '1BHK',
                'price': 8500000,
                'carpet_area': 450,
                'bathrooms': 2,
                'balcony': 1,
                'furnished_type': 'UNFURNISHED',
                'possession_date': '2025-09-28',
                'project_summary': 'Luxury apartments in Chembur'
            },
            {
                'project_id': 'sample_2',
                'project_name': 'Ashwini',
                'project_type': 'RESIDENTIAL', 
                'status': 'UNDER_CONSTRUCTION',
                'city': 'Mumbai',
                'locality': 'Chembur',
                'bhk_type': '2BHK',
                'price': 12000000,
                'carpet_area': 650,
                'bathrooms': 2,
                'balcony': 2,
                'furnished_type': 'UNFURNISHED',
                'possession_date': '2025-09-28',
                'project_summary': 'Luxury apartments in Chembur'
            },
            {
                'project_id': 'sample_3',
                'project_name': 'Pristine02',
                'project_type': 'RESIDENTIAL',
                'status': 'READY_TO_MOVE',
                'city': 'Pune',
                'locality': 'Shivajinagar',
                'bhk_type': '2BHK',
                'price': 12000000,
                'carpet_area': 972,
                'bathrooms': 3,
                'balcony': 2,
                'furnished_type': 'UNFURNISHED',
                'possession_date': '',
                'project_summary': 'Ready to move apartments in Pune'
            },
            {
                'project_id': 'sample_4',
                'project_name': 'Pristine02',
                'project_type': 'RESIDENTIAL',
                'status': 'READY_TO_MOVE', 
                'city': 'Pune',
                'locality': 'Shivajinagar',
                'bhk_type': '3BHK',
                'price': 18000000,
                'carpet_area': 1200,
                'bathrooms': 3,
                'balcony': 3,
                'furnished_type': 'SEMI_FURNISHED',
                'possession_date': '',
                'project_summary': 'Ready to move apartments in Pune'
            },
            {
                'project_id': 'sample_5',
                'project_name': 'Gurukripa',
                'project_type': 'RESIDENTIAL',
                'status': 'UNDER_CONSTRUCTION',
                'city': 'Mumbai',
                'locality': 'Chembur',
                'bhk_type': '3BHK',
                'price': 29000000,
                'carpet_area': 893,
                'bathrooms': 3,
                'balcony': 2,
                'furnished_type': 'UNFURNISHED',
                'possession_date': '',
                'project_summary': 'Under construction project in Mumbai'
            }
        ]
        
        for prop_data in sample_properties:
            PropertyListing.objects.create(**prop_data)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Loaded {len(sample_properties)} sample properties!'))
        self.stdout.write("🏠 Now you can test queries like: '3BHK flat in Pune under ₹1.2 Cr'")