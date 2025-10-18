from django.core.management.base import BaseCommand
from property_search.data_loader import DataLoader

class Command(BaseCommand):
    help = 'Load property data from CSV files'
    
    def handle(self, *args, **options):
        self.stdout.write("🚀 STARTING DATA LOADING FROM YOUR CSV FILES")
        self.stdout.write("=" * 60)
        
        loader = DataLoader()
        success = loader.load_all_data()
        
        if success:
            self.stdout.write(self.style.SUCCESS("✅ DATA LOADING COMPLETED SUCCESSFULLY!"))
        else:
            self.stdout.write(self.style.ERROR("❌ DATA LOADING FAILED!"))
            self.stdout.write("💡 Please make sure:")
            self.stdout.write("   1. The 'data' folder exists in the backend directory")
            self.stdout.write("   2. All 4 CSV files are in the data folder")
            self.stdout.write("   3. The CSV files have the correct names")