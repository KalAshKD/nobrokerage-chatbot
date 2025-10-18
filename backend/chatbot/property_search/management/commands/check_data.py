from django.core.management.base import BaseCommand
from property_search.models import PropertyListing

class Command(BaseCommand):
    help = 'Check what data is loaded in the database'
    
    def handle(self, *args, **options):
        total_properties = PropertyListing.objects.count()
        self.stdout.write("=" * 50)
        self.stdout.write("📊 DATABASE CHECK")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Total properties in database: {total_properties}")
        
        if total_properties == 0:
            self.stdout.write(self.style.WARNING("❌ No properties found in database!"))
            self.stdout.write("Run: python manage.py load_data")
            return
        
        self.stdout.write(f"\n🏙️ Cities distribution:")
        cities = PropertyListing.objects.values_list('city', flat=True).distinct()
        for city in cities:
            count = PropertyListing.objects.filter(city=city).count()
            self.stdout.write(f"  - {city}: {count} properties")
        
        self.stdout.write(f"\n🏠 BHK types distribution:")
        bhk_types = PropertyListing.objects.values_list('bhk_type', flat=True).distinct()
        for bhk in bhk_types:
            if bhk:
                count = PropertyListing.objects.filter(bhk_type=bhk).count()
                self.stdout.write(f"  - {bhk}: {count} properties")
        
        self.stdout.write(f"\n📅 Status distribution:")
        statuses = PropertyListing.objects.values_list('status', flat=True).distinct()
        for status in statuses:
            count = PropertyListing.objects.filter(status=status).count()
            self.stdout.write(f"  - {status}: {count} properties")
        
        self.stdout.write(f"\n📋 Sample properties (first 5):")
        for prop in PropertyListing.objects.all()[:5]:
            price_display = f"₹{prop.price:,.0f}" if prop.price else "Price not set"
            self.stdout.write(f"  - {prop.project_name} | {prop.bhk_type} | {prop.city} | {price_display} | {prop.status}")