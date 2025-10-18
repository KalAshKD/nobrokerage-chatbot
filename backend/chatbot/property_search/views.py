from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .query_parser import QueryParser
from .models import PropertyListing
from .summarizer import SummaryGenerator
import math
import traceback



from django.shortcuts import render

def chat_interface(request):
    return render(request, 'chat_interface.html')



@csrf_exempt
@require_http_methods(["POST"])
def chat_query(request):
    try:
        data = json.loads(request.body)
        user_query = data.get('query', '')
        
        print(f"🔍 Received query: {user_query}")
        
        # Parse user query
        parser = QueryParser()
        filters = parser.parse_query(user_query)
        
        print(f"🎯 Parsed filters: {filters}")
        
        # Search for properties
        properties = search_properties(filters)
        
        print(f"📊 Found {len(properties)} properties")
        
        # Generate summary
        summarizer = SummaryGenerator()
        summary = summarizer.generate_summary(properties, filters)
        
        # Format response
        response_data = {
            'summary': summary,
            'filters_applied': filters,
            'properties': format_properties(properties),
            'total_results': len(properties)
        }
        
        print(f"✅ Successfully processed query")
        return JsonResponse(response_data)
    
    except Exception as e:
        print(f"❌ Error in chat_query: {str(e)}")
        print("🔍 Full traceback:")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

def search_properties(filters):
    """Search properties based on filters"""
    print("🔍 Starting property search...")
    properties = PropertyListing.objects.all()
    
    print(f"📈 Total properties in DB: {properties.count()}")
    
    # Apply city filter
    if 'city' in filters:
        print(f"🏙️ Applying city filter: {filters['city']}")
        properties = properties.filter(city__icontains=filters['city'])
        print(f"📊 After city filter: {properties.count()} properties")
    
    # Apply BHK filter
    if 'bhk' in filters:
        bhk_value = filters['bhk'].replace('BHK', '').strip()
        print(f"🏠 Applying BHK filter: {bhk_value}")
        properties = properties.filter(bhk_type__icontains=bhk_value)
        print(f"📊 After BHK filter: {properties.count()} properties")
    
    # Apply budget filter
    if 'budget' in filters:
        max_price = filters['budget'] * 100000  # Convert lakhs to actual price
        print(f"💰 Applying budget filter: ₹{filters['budget']}L (max price: {max_price})")
        properties = properties.filter(price__lte=max_price)
        print(f"📊 After budget filter: {properties.count()} properties")
    
    # Apply status filter
    if 'status' in filters:
        print(f"📅 Applying status filter: {filters['status']}")
        properties = properties.filter(status=filters['status'])
        print(f"📊 After status filter: {properties.count()} properties")
    
    # Apply locality filter
    if 'locality' in filters:
        print(f"📍 Applying locality filter: {filters['locality']}")
        properties = properties.filter(locality__icontains=filters['locality'])
        print(f"📊 After locality filter: {properties.count()} properties")
    
    results = list(properties[:20])  # Limit results
    print(f"🎯 Final results: {len(results)} properties")
    return results

def format_properties(properties):
    """Format properties for frontend display"""
    formatted = []
    for prop in properties:
        try:
            # Get first image if available
            images = []
            if prop.property_images and prop.property_images != '[]':
                try:
                    # Handle different image format cases
                    images_str = prop.property_images
                    if images_str.startswith('[') and images_str.endswith(']'):
                        images = json.loads(images_str)
                    else:
                        images = [images_str]
                except:
                    images = [prop.property_images] if prop.property_images else []
            
            image_url = images[0] if images else ''
            
            # Format price safely
            price_display = 'Price on request'
            if prop.price:
                try:
                    price_display = format_price(float(prop.price))
                except (ValueError, TypeError):
                    price_display = 'Price on request'
            
            # Format area safely
            area_display = 'Area not specified'
            if prop.carpet_area:
                try:
                    area_display = f"{float(prop.carpet_area):.0f} sq.ft."
                except (ValueError, TypeError):
                    area_display = 'Area not specified'
            
            formatted.append({
                'id': prop.project_id,
                'title': f"{prop.project_name} - {prop.bhk_type}",
                'city': prop.city or 'City not specified',
                'locality': prop.locality or 'Location not specified',
                'bhk': prop.bhk_type or 'Type not specified',
                'price': price_display,
                'project_name': prop.project_name or 'Unknown Project',
                'status': prop.status.replace('_', ' ').title() if prop.status else 'Status not specified',
                'possession_date': prop.possession_date if prop.possession_date else 'TBD',
                'amenities': get_amenities(prop),
                'url': f"/project/{prop.slug}" if prop.slug else "#",
                'carpet_area': area_display,
                'image': image_url,
                'bathrooms': prop.bathrooms if prop.bathrooms else 'N/A',
                'balcony': prop.balcony if prop.balcony else 'N/A'
            })
        except Exception as e:
            print(f"⚠️ Error formatting property {prop.project_id}: {e}")
            continue
    
    return formatted

def format_price(price):
    """Format price in Cr/Lakh"""
    if not price or price <= 0:
        return "Price on request"
    
    if price >= 10000000:  # 1 Crore
        return f"₹{price/10000000:.1f} Cr"
    elif price >= 100000:  # 1 Lakh
        return f"₹{price/100000:.1f} L"
    else:
        return f"₹{price:,.0f}"

def get_amenities(property_obj):
    """Generate amenities based on property features"""
    amenities = []
    
    if property_obj.bathrooms and property_obj.bathrooms >= 2:
        amenities.append(f"{property_obj.bathrooms} Bathrooms")
    elif property_obj.bathrooms:
        amenities.append(f"{property_obj.bathrooms} Bathroom")
    
    if property_obj.balcony and property_obj.balcony > 0:
        amenities.append(f"{property_obj.balcony} Balcony")
    
    if property_obj.furnished_type and property_obj.furnished_type != 'UNFURNISHED':
        amenities.append(property_obj.furnished_type.title())
    
    # Add some default amenities based on project type
    if 'luxury' in (property_obj.project_name or '').lower():
        amenities.extend(['Swimming Pool', 'Gym', 'Park'])
    else:
        amenities.extend(['Parking', 'Security'])
    
    return amenities[:3]  # Return top 3 amenities




def search_properties(filters):
    """Search properties based on filters"""
    print("🔍 Starting property search...")
    properties = PropertyListing.objects.all()
    
    print(f"📈 Total properties in DB: {properties.count()}")
    
    # Apply city filter
    if 'city' in filters:
        print(f"🏙️ Applying city filter: {filters['city']}")
        properties = properties.filter(city__icontains=filters['city'])
        print(f"📊 After city filter: {properties.count()} properties")
    
    # Apply BHK filter - FIXED: Handle different BHK formats
    if 'bhk' in filters:
        bhk_value = filters['bhk'].replace('BHK', '').strip()
        print(f"🏠 Applying BHK filter: {bhk_value}")
        
        # Try exact match first
        exact_match = properties.filter(bhk_type__iexact=filters['bhk'])
        if exact_match.exists():
            properties = exact_match
        else:
            # Fallback to contains search
            properties = properties.filter(bhk_type__icontains=bhk_value)
        
        print(f"📊 After BHK filter: {properties.count()} properties")
    
    # Apply budget filter
    if 'budget' in filters:
        max_price = filters['budget'] * 100000  # Convert lakhs to actual price
        print(f"💰 Applying budget filter: ₹{filters['budget']}L (max price: {max_price})")
        properties = properties.filter(price__lte=max_price)
        print(f"📊 After budget filter: {properties.count()} properties")
    
    # Apply status filter
    if 'status' in filters:
        print(f"📅 Applying status filter: {filters['status']}")
        properties = properties.filter(status=filters['status'])
        print(f"📊 After status filter: {properties.count()} properties")
    
    # Apply locality filter
    if 'locality' in filters:
        print(f"📍 Applying locality filter: {filters['locality']}")
        properties = properties.filter(locality__icontains=filters['locality'])
        print(f"📊 After locality filter: {properties.count()} properties")
    
    results = list(properties[:50])  # Increased limit to show more results
    print(f"🎯 Final results: {len(results)} properties")
    return results