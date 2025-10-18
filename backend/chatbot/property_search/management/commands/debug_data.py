from django.core.management.base import BaseCommand
import pandas as pd
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Debug: Check CSV files and their contents'
    
    def handle(self, *args, **options):
        # Get the base directory
        base_dir = settings.BASE_DIR
        data_dir = os.path.join(base_dir, 'data')
        
        self.stdout.write("=" * 60)
        self.stdout.write("🔍 DEBUG DATA CHECK")
        self.stdout.write("=" * 60)
        self.stdout.write(f"📁 Base directory: {base_dir}")
        self.stdout.write(f"📁 Data directory: {data_dir}")
        
        # Check if directory exists
        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR("❌ Data directory does not exist!"))
            self.stdout.write("Please make sure you have a 'data' folder with these files:")
            self.stdout.write("  - project.csv")
            self.stdout.write("  - ProjectAddress.csv") 
            self.stdout.write("  - ProjectConfiguration.csv")
            self.stdout.write("  - ProjectConfigurationVariant.csv")
            return
        
        # List files
        files = os.listdir(data_dir)
        self.stdout.write(f"\n📂 Files found in data directory: {files}")
        
        # Check each required CSV file
        required_files = ['project.csv', 'ProjectAddress.csv', 'ProjectConfiguration.csv', 'ProjectConfigurationVariant.csv']
        
        for csv_file in required_files:
            filepath = os.path.join(data_dir, csv_file)
            self.stdout.write(f"\n" + "=" * 50)
            self.stdout.write(f"🔍 Checking: {csv_file}")
            self.stdout.write("=" * 50)
            
            if not os.path.exists(filepath):
                self.stdout.write(self.style.ERROR(f"   ❌ FILE NOT FOUND: {csv_file}"))
                continue
            
            try:
                # Get file size
                file_size = os.path.getsize(filepath)
                self.stdout.write(f"   ✅ File exists: {file_size} bytes")
                
                # Try to read the CSV
                df = pd.read_csv(filepath)
                self.stdout.write(f"   ✅ Loaded successfully: {len(df)} rows, {len(df.columns)} columns")
                
                # Show columns
                self.stdout.write(f"   📊 Columns: {list(df.columns)}")
                
                # Show first 2 rows
                self.stdout.write(f"   📋 First 2 rows:")
                for idx, row in df.head(2).iterrows():
                    self.stdout.write(f"      Row {idx}: {row.to_dict()}")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ ERROR loading {csv_file}: {str(e)}"))
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("✅ Debug check completed")
        self.stdout.write("=" * 60)