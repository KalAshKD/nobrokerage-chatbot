import pandas as pd
import os
from django.conf import settings
from .models import PropertyListing

class DataLoader:
    def __init__(self):
        # Fix the path - data folder should be in backend/, not backend/chatbot/
        self.data_dir = os.path.join(settings.BASE_DIR, '..', 'data')
        print(f"📁 Looking for data in: {self.data_dir}")
        
        # Also check if it exists
        if os.path.exists(self.data_dir):
            print("✅ Data directory exists!")
            files = os.listdir(self.data_dir)
            print(f"📂 Files found: {files}")
        else:
            print("❌ Data directory not found at this location")
    
    def load_all_data(self):
        """Load data from all 4 CSV files"""
        print("🔄 Starting data loading from all 4 CSV files...")
        
        # Clear existing data
        PropertyListing.objects.all().delete()
        print("🗑️ Cleared existing data")
        
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            print(f"❌ Data directory not found: {self.data_dir}")
            print("💡 Please create the data folder here:")
            print(f"💡 {self.data_dir}")
            return False
        
        # Check if all required files exist
        required_files = [
            'project.csv',
            'ProjectAddress.csv', 
            'ProjectConfiguration.csv',
            'ProjectConfigurationVariant.csv'
        ]
        
        # Check each file
        for file in required_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                print(f"✅ Found: {file}")
            else:
                print(f"❌ Missing: {file}")
        
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(self.data_dir, f))]
        
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
            return False
        
        try:
            # Load all CSV files
            print("📖 Reading CSV files...")
            projects_df = pd.read_csv(os.path.join(self.data_dir, 'project.csv'))
            addresses_df = pd.read_csv(os.path.join(self.data_dir, 'ProjectAddress.csv'))
            configs_df = pd.read_csv(os.path.join(self.data_dir, 'ProjectConfiguration.csv'))
            variants_df = pd.read_csv(os.path.join(self.data_dir, 'ProjectConfigurationVariant.csv'))
            
            print(f"✅ Loaded CSV files:")
            print(f"   - projects: {len(projects_df)} rows")
            print(f"   - addresses: {len(addresses_df)} rows")
            print(f"   - configurations: {len(configs_df)} rows") 
            print(f"   - variants: {len(variants_df)} rows")
            
            # Fill NaN values
            projects_df = projects_df.fillna('')
            addresses_df = addresses_df.fillna('')
            configs_df = configs_df.fillna('')
            variants_df = variants_df.fillna('')
            
            property_count = 0
            
            # Process each project
            for _, project in projects_df.iterrows():
                project_id = project['id']
                project_name = project.get('projectName', 'Unknown Project')
                
                # FIX: Properly handle empty DataFrames
                project_addresses = addresses_df[addresses_df['projectId'] == project_id]
                if len(project_addresses) > 0:
                    address = project_addresses.iloc[0].to_dict()
                else:
                    address = {}
                
                # Find configurations for this project
                project_configs = configs_df[configs_df['projectId'] == project_id]
                
                if len(project_configs) > 0:
                    print(f"🏢 Processing: {project_name} ({len(project_configs)} configurations)")
                
                for _, config in project_configs.iterrows():
                    config_id = config['id']
                    
                    # Find variants for this configuration
                    config_variants = variants_df[variants_df['configurationId'] == config_id]
                    
                    if len(config_variants) == 0:
                        # Create property from config only
                        if self._create_property(project.to_dict(), config.to_dict(), address, None):
                            property_count += 1
                    else:
                        for _, variant in config_variants.iterrows():
                            if self._create_property(project.to_dict(), config.to_dict(), address, variant.to_dict()):
                                property_count += 1
            
            print(f"🎉 SUCCESS: Loaded {property_count} properties from your CSV files!")
            return True
            
        except Exception as e:
            print(f"❌ ERROR loading data: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_property(self, project, config, address, variant):
        """Create a property listing from CSV data"""
        try:
            # Create unique ID
            unique_id = f"{project['id']}_{config['id']}"
            if variant is not None:
                unique_id += f"_{variant['id']}"
            
            # Determine city from slug or address
            city = self._extract_city(project, address)
            
            # Get BHK type
            bhk_type = config.get('type', '')
            if not bhk_type:
                bhk_type = config.get('customBHK', 'Unknown')
            
            # Get price and area from variant
            price = self._safe_float(variant.get('price')) if variant else None
            carpet_area = self._safe_float(variant.get('carpetArea')) if variant else None
            
            # Get other details
            bathrooms = self._safe_int(variant.get('bathrooms')) if variant else None
            balcony = self._safe_int(variant.get('balcony')) if variant else None
            furnished_type = variant.get('furnishedType', 'UNFURNISHED') if variant else 'UNFURNISHED'
            property_images = variant.get('propertyImages', '[]') if variant else '[]'
            
            # Create the property
            PropertyListing.objects.create(
                project_id=unique_id,
                project_name=project.get('projectName', 'Unknown Project'),
                project_type=project.get('projectType', 'RESIDENTIAL'),
                status=project.get('status', 'UNDER_CONSTRUCTION'),
                possession_date=str(project.get('possessionDate', ''))[:50],
                project_summary=project.get('projectSummary', ''),
                slug=project.get('slug', ''),
                city=city,
                locality=address.get('landmark', '')[:100],
                full_address=address.get('fullAddress', ''),
                landmark=address.get('landmark', ''),
                pincode=str(address.get('pincode', '')),
                bhk_type=bhk_type,
                property_category=config.get('propertyCategory', 'RESIDENTIAL'),
                price=price,
                carpet_area=carpet_area,
                bathrooms=bathrooms,
                balcony=balcony,
                furnished_type=furnished_type,
                property_images=property_images,
            )
            
            print(f"   ✅ Created: {project.get('projectName')} - {bhk_type} in {city}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error creating property {project.get('projectName', 'Unknown')}: {e}")
            return False
    
    def _extract_city(self, project, address):
        """Extract city from project data"""
        # Try from slug first
        slug = str(project.get('slug', '')).lower()
        if 'pune' in slug:
            return 'Pune'
        elif 'mumbai' in slug:
            return 'Mumbai'
        
        # Try from address
        address_str = str(address.get('fullAddress', '')).lower()
        if 'pune' in address_str:
            return 'Pune'
        elif 'mumbai' in address_str:
            return 'Mumbai'
        
        # Default to Mumbai
        return 'Mumbai'
    
    def _safe_float(self, value):
        """Safely convert to float"""
        try:
            if value and str(value).strip() and str(value) != 'nan':
                return float(value)
        except (ValueError, TypeError):
            return None
    
    def _safe_int(self, value):
        """Safely convert to int"""
        try:
            if value and str(value).strip() and str(value) != 'nan':
                return int(float(value))
        except (ValueError, TypeError):
            return None