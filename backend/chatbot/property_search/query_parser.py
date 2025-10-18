import re

class QueryParser:
    def __init__(self):
        self.cities = ['pune', 'mumbai', 'delhi', 'bangalore']
        self.bhk_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:bhk|bedroom|bed|bedrooms)',
            r'(\d+)\s*(?:room|rk|rooms)'
        ]
        self.budget_patterns = [
            r'under\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:cr|lakh|crore|l|laksh)',
            r'less\s*than\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:cr|lakh|crore|l)',
            r'upto\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:cr|lakh|crore|l)',
            r'budget\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:cr|lakh|crore|l)',
            r'(\d+(?:\.\d+)?)\s*(?:cr|lakh|crore)\s*(?:and\s*below|or\s*less|max)'
        ]
    
    def parse_query(self, query):
        """Extract filters from natural language query"""
        query_lower = query.lower()
        
        filters = {
            'city': self._extract_city(query_lower),
            'bhk': self._extract_bhk(query_lower),
            'budget': self._extract_budget(query_lower),
            'status': self._extract_status(query_lower),
            'locality': self._extract_locality(query_lower),
            'project_name': self._extract_project_name(query_lower),
            'amenities': self._extract_amenities(query_lower)
        }
        
        # Clean None values
        return {k: v for k, v in filters.items() if v is not None}
    
    def _extract_city(self, query):
        for city in self.cities:
            if city in query:
                return city.title()
        return None
    
    def _extract_bhk(self, query):
        for pattern in self.bhk_patterns:
            matches = re.findall(pattern, query)
            if matches:
                bhk_value = matches[0]
                # Convert to proper BHK format without decimal if whole number
                try:
                    bhk_float = float(bhk_value)
                    if bhk_float.is_integer():
                        return f"{int(bhk_float)}BHK"
                    else:
                        return f"{bhk_float}BHK"
                except ValueError:
                    return f"{bhk_value}BHK"
        return None
    
    def _extract_budget(self, query):
        # First check for crore patterns
        crore_patterns = [
            r'[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:cr|crore)',
            r'(\d+(?:\.\d+)?)\s*(?:cr|crore)',
        ]
        
        for pattern in crore_patterns:
            match = re.search(pattern, query)
            if match:
                amount = float(match.group(1))
                return amount * 100  # Convert crore to lakh
        
        # Then check for lakh patterns
        lakh_patterns = [
            r'under\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac|l)',
            r'less\s*than\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac|l)',
            r'upto\s*[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac|l)',
            r'[₹rs]?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac|l)',
        ]
        
        for pattern in lakh_patterns:
            match = re.search(pattern, query)
            if match:
                return float(match.group(1))
        
        return None
    
    def _extract_status(self, query):
        if 'ready' in query or 'possession' in query or 'move' in query or 'immediate' in query:
            return 'READY_TO_MOVE'
        elif 'under construction' in query or 'construction' in query or 'upcoming' in query:
            return 'UNDER_CONSTRUCTION'
        return None
    
    def _extract_locality(self, query):
        # Common localities in Pune and Mumbai
        pune_localities = ['wakad', 'baner', 'hinjewadi', 'kharadi', 'viman nagar', 'ravet', 'camp', 
                          'koregaon park', 'aundh', 'hadapsar', 'kothrud', 'shivajinagar', 'model colony']
        mumbai_localities = ['chembur', 'andheri', 'bandra', 'powai', 'ghatkopar', 'borivali', 'dadar',
                            'worli', 'lower parel', 'juhu', 'versova']
        
        all_localities = pune_localities + mumbai_localities
        for locality in all_localities:
            if locality in query:
                return locality.title()
        return None
    
    def _extract_project_name(self, query):
        # Look for capitalized words that might be project names
        words = query.split()
        potential_names = []
        for word in words:
            if (word[0].isupper() and len(word) > 3 and 
                word.lower() not in self.cities and 
                not any(loc in word.lower() for loc in ['bhk', 'cr', 'lakh', 'crore'])):
                potential_names.append(word)
        return ' '.join(potential_names) if potential_names else None
    
    def _extract_amenities(self, query):
        amenities_keywords = {
            'swimming': 'Swimming Pool',
            'pool': 'Swimming Pool',
            'gym': 'Gym',
            'garden': 'Garden',
            'park': 'Park',
            'security': 'Security',
            'lift': 'Lift',
            'parking': 'Parking',
            'club': 'Clubhouse',
            'play': 'Play Area',
            'metro': 'Metro Access',
            'school': 'School Nearby',
            'hospital': 'Hospital Nearby'
        }
        
        found_amenities = []
        for keyword, amenity in amenities_keywords.items():
            if keyword in query:
                found_amenities.append(amenity)
        
        return found_amenities if found_amenities else None