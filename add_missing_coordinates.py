#!/usr/bin/env python3
import json
from geopy.geocoders import Nominatim
import time

def add_missing_coordinates():
    """Add coordinates for organizations that are missing them"""
    
    # Load existing data
    with open('knight_organizations_processed.json', 'r') as f:
        organizations = json.load(f)
    
    geolocator = Nominatim(user_agent="knight_impact_mapper_v2")
    
    # Manual coordinate assignments for known organizations
    manual_coords = {
        # LA Fire Response Organizations
        "World Centeral Kitchen (LA Fire Response)": {
            "lat": 34.0522, "lng": -118.2437, 
            "city": "Los Angeles", "state": "CA", "city_category": "los_angeles"
        },
        "American Red Cross (LA Fire Response)": {
            "lat": 34.0522, "lng": -118.2437,
            "city": "Los Angeles", "state": "CA", "city_category": "los_angeles"
        },
        
        # Chicago-based organizations (use Chicago coordinates)
        "Alzheimer's Association": {
            "lat": 41.8781, "lng": -87.6298,
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Chicago Funders Together to End Homelesssness": {
            "lat": 41.8781, "lng": -87.6298,
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Crossroads Fund": {
            "lat": 41.8781, "lng": -87.6298,
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Greater Chicago Food Depository / City Colleges of Chicago  Partnership": {
            "lat": 41.8781, "lng": -87.6298,
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Forefront": {
            "lat": 41.8781, "lng": -87.6298,
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Imagine Englewood If": {
            "lat": 41.7794, "lng": -87.6431,  # Englewood neighborhood
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Reclaiming Chicago": {
            "lat": 41.8781, "lng": -87.6298,
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        
        # National organizations (use DC coordinates)
        "National Alliance to End Homelessness": {
            "lat": 38.9072, "lng": -77.0369,
            "city": "Washington", "state": "DC", "city_category": "other"
        },
        
        # Other organizations - try to geocode or use reasonable defaults
        "One Acre Fund": {
            "lat": 41.8781, "lng": -87.6298,  # Has Chicago presence
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        },
        "Window to the World": {
            "lat": 41.8781, "lng": -87.6298,  # Chicago public media
            "city": "Chicago", "state": "IL", "city_category": "chicago"
        }
    }
    
    updated_count = 0
    
    for org in organizations:
        # Skip if already has coordinates
        if org.get('lat') and org.get('lng'):
            continue
            
        org_name = org['name']
        print(f"Processing: {org_name}")
        
        # Check if we have manual coordinates
        if org_name in manual_coords:
            coords = manual_coords[org_name]
            org.update(coords)
            print(f"  ✅ Added manual coordinates: {coords['lat']}, {coords['lng']} ({coords['city']}, {coords['state']})")
            updated_count += 1
            continue
        
        # Try to geocode based on organization name for well-known orgs
        try:
            # For organizations with location hints in name
            search_terms = []
            
            if "chicago" in org_name.lower():
                search_terms.append(f"{org_name}, Chicago, IL")
            elif "la " in org_name.lower() or "los angeles" in org_name.lower():
                search_terms.append(f"{org_name}, Los Angeles, CA")
            else:
                search_terms.append(f"{org_name}, United States")
            
            for search_term in search_terms:
                print(f"  🔍 Searching: {search_term}")
                location = geolocator.geocode(search_term, timeout=10)
                
                if location:
                    org['lat'] = location.latitude
                    org['lng'] = location.longitude
                    
                    # Determine city category based on coordinates
                    if location.latitude > 33 and location.latitude < 35 and location.longitude > -119 and location.longitude < -117:
                        org['city_category'] = 'los_angeles'
                        if not org.get('city'):
                            org['city'] = 'Los Angeles'
                        if not org.get('state'):
                            org['state'] = 'CA'
                    elif location.latitude > 41 and location.latitude < 43 and location.longitude > -88 and location.longitude < -87:
                        org['city_category'] = 'chicago'
                        if not org.get('city'):
                            org['city'] = 'Chicago'
                        if not org.get('state'):
                            org['state'] = 'IL'
                    else:
                        org['city_category'] = 'other'
                    
                    print(f"  ✅ Geocoded: {location.latitude}, {location.longitude}")
                    updated_count += 1
                    break
                
                time.sleep(0.5)  # Be respectful to geocoding service
                
        except Exception as e:
            print(f"  ❌ Geocoding failed: {e}")
        
        # If still no coordinates, assign default based on name patterns
        if not org.get('lat'):
            if any(term in org_name.lower() for term in ['chicago', 'englewood', 'illinois']):
                org.update({
                    'lat': 41.8781, 'lng': -87.6298,
                    'city': 'Chicago', 'state': 'IL', 'city_category': 'chicago'
                })
                print(f"  📍 Default Chicago coordinates assigned")
                updated_count += 1
            elif any(term in org_name.lower() for term in ['la', 'los angeles', 'california']):
                org.update({
                    'lat': 34.0522, 'lng': -118.2437,
                    'city': 'Los Angeles', 'state': 'CA', 'city_category': 'los_angeles'
                })
                print(f"  📍 Default LA coordinates assigned")
                updated_count += 1
    
    # Save updated data
    with open('knight_organizations_processed.json', 'w') as f:
        json.dump(organizations, f, indent=2, default=str)
    
    print(f"\n✅ Updated {updated_count} organizations with coordinates")
    
    # Print summary by city
    cities = {}
    for org in organizations:
        city_cat = org.get('city_category', 'other')
        if city_cat not in cities:
            cities[city_cat] = 0
        cities[city_cat] += 1
    
    print(f"\nFinal distribution:")
    for city, count in cities.items():
        print(f"  {city}: {count} organizations")

if __name__ == "__main__":
    add_missing_coordinates()
