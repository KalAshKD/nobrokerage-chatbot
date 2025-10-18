class SummaryGenerator:
    def generate_summary(self, properties, filters):
        if not properties:
            return self._no_results_summary(filters)
        
        total_properties = len(properties)
        
        # Calculate statistics
        prices = [float(prop.price) for prop in properties if prop.price]
        areas = [float(prop.carpet_area) for prop in properties if prop.carpet_area]
        
        # Collect unique features
        cities = set(prop.city for prop in properties if prop.city)
        localities = set(prop.locality for prop in properties if prop.locality)
        statuses = set(prop.status for prop in properties if prop.status)
        bhk_types = set(prop.bhk_type for prop in properties if prop.bhk_type)
        
        # Build comprehensive summary
        summary_parts = []
        
        # Introduction with count
        if total_properties == 1:
            summary_parts.append("I found 1 property")
        else:
            summary_parts.append(f"I found {total_properties} properties")
        
        # Add BHK information
        if bhk_types:
            if len(bhk_types) == 1:
                summary_parts.append(f"with {list(bhk_types)[0]} configuration")
            else:
                bhk_list = list(bhk_types)[:3]
                if len(bhk_list) == 1:
                    summary_parts.append(f"with {bhk_list[0]} configuration")
                else:
                    summary_parts.append(f"with {', '.join(bhk_list[:-1])} and {bhk_list[-1]} options")
        
        # Add location details
        if localities:
            loc_list = list(localities)[:3]
            if len(loc_list) == 1:
                summary_parts.append(f"in {loc_list[0]}")
            elif len(loc_list) == 2:
                summary_parts.append(f"in {loc_list[0]} and {loc_list[1]}")
            else:
                summary_parts.append(f"in areas like {', '.join(loc_list[:-1])}, and {loc_list[-1]}")
        elif cities:
            if len(cities) == 1:
                summary_parts.append(f"in {list(cities)[0]}")
            else:
                summary_parts.append(f"across {', '.join(cities)}")
        
        # Add price range
        if prices:
            min_price_lakh = min(prices) / 100000
            max_price_lakh = max(prices) / 100000
            if min_price_lakh == max_price_lakh:
                summary_parts.append(f"priced at ₹{min_price_lakh:.1f}L")
            else:
                summary_parts.append(f"with prices ranging from ₹{min_price_lakh:.1f}L to ₹{max_price_lakh:.1f}L")
        
        # Add area information
        if areas:
            avg_area = sum(areas) / len(areas)
            summary_parts.append(f"and average carpet area of {avg_area:.0f} sq.ft.")
        
        # Add status information
        if statuses:
            if len(statuses) == 1:
                status = list(statuses)[0].replace('_', ' ').title()
                summary_parts.append(f"(all {status})")
            else:
                status_desc = "mix of " + " and ".join([s.replace('_', ' ').lower() for s in statuses])
                summary_parts.append(f"({status_desc})")
        
        # Construct the final summary
        summary = ' '.join(summary_parts) + '.'
        
        # Add specific highlights
        if total_properties >= 3:
            if prices and 'budget' in filters:
                affordable_count = len([p for p in prices if p <= filters.get('budget', float('inf')) * 100000])
                if affordable_count >= total_properties * 0.8:
                    summary += " Most options fit well within your budget."
                elif affordable_count <= total_properties * 0.3:
                    summary += " Consider expanding your budget for more options."
            
            if areas:
                large_properties = len([a for a in areas if a > 1000])
                if large_properties >= total_properties * 0.6:
                    summary += " Many properties offer spacious living areas."
        
        return summary
    
    def _no_results_summary(self, filters):
        """Generate helpful summary when no properties found"""
        base_msg = "I couldn't find any properties"
        
        conditions = []
        if 'bhk' in filters:
            conditions.append(f"{filters['bhk']}")
        if 'city' in filters:
            conditions.append(f"in {filters['city']}")
        if 'budget' in filters:
            conditions.append(f"under ₹{filters['budget']}L")
        if 'status' in filters:
            conditions.append(filters['status'].replace('_', ' ').lower())
        if 'locality' in filters:
            conditions.append(f"in {filters['locality']}")
        
        if conditions:
            base_msg += " matching " + ", ".join(conditions)
        
        # Provide helpful suggestions based on available data
        suggestions = []
        if 'budget' in filters and filters['budget'] < 50:
            suggestions.append("consider increasing your budget")
        if 'bhk' in filters and '3' in filters['bhk']:
            suggestions.append("try searching for 2BHK options")
        if 'locality' in filters:
            suggestions.append("expand your search to nearby areas")
        if 'status' in filters:
            suggestions.append("try both ready-to-move and under-construction properties")
        
        if suggestions:
            base_msg += ". You might want to " + ", ".join(suggestions) + "."
        else:
            base_msg += ". Try adjusting your search criteria for better results."
        
        return base_msg