from django.core.management.base import BaseCommand
from property_search.data_loader import DataLoader

class Command(BaseCommand):
    help = 'Load property data from all 4 CSV files'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting property data loading from all CSV files...')
        loader = DataLoader()
        loader.load_all_data()
        self.stdout.write(
            self.style.SUCCESS('✅ Data loading completed!')
        )