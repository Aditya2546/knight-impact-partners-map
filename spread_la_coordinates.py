#!/usr/bin/env python3
import json

def spread_la_coordinates():
    """Spread LA organizations across different LA locations"""
    
    # Load existing data
    with open('knight_organizations_processed.json', 'r') as f:
        organizations = json.load(f)
    
    # Different LA area coordinates to spread organizations
    la_locations = {
        "Inclusive Economy Lab": {
            "lat": 34.0522, "lng": -118.2437,  # Downtown LA
            "location_name": "Downtown Los Angeles"
        },
        "World Centeral Kitchen (LA Fire Response)": [
            {
                "lat": 34.0928, "lng": -118.3287,  # Hollywood
                "location_name": "Hollywood"
            },
            {
                "lat": 34.0195, "lng": -118.4912,  # Santa Monica
                "location_name": "Santa Monica"
            }
        ],
        "American Red Cross (LA Fire Response)": {
            "lat": 34.0736, "lng": -118.4004,  # Beverly Hills
            "location_name": "Beverly Hills"
        }
    }
    
    updated_count = 0
    world_kitchen_count = 0
    
    for org in organizations:
        if org.get('city_category') == 'los_angeles':
            org_name = org['name']
            print(f"Processing: {org_name}")
            
            if org_name == "Inclusive Economy Lab":
                coords = la_locations[org_name]
                org['lat'] = coords['lat']
                org['lng'] = coords['lng']
                org['location_note'] = coords['location_name']
                print(f"  ✅ Updated to {coords['location_name']}: {coords['lat']}, {coords['lng']}")
                updated_count += 1
                
            elif org_name == "World Centeral Kitchen (LA Fire Response)":
                # Use different coordinates for each World Central Kitchen entry
                coords = la_locations[org_name][world_kitchen_count % 2]
                org['lat'] = coords['lat']
                org['lng'] = coords['lng']
                org['location_note'] = coords['location_name']
                print(f"  ✅ Updated to {coords['location_name']}: {coords['lat']}, {coords['lng']}")
                world_kitchen_count += 1
                updated_count += 1
                
            elif org_name == "American Red Cross (LA Fire Response)":
                coords = la_locations[org_name]
                org['lat'] = coords['lat']
                org['lng'] = coords['lng']
                org['location_note'] = coords['location_name']
                print(f"  ✅ Updated to {coords['location_name']}: {coords['lat']}, {coords['lng']}")
                updated_count += 1
    
    # Save updated data
    with open('knight_organizations_processed.json', 'w') as f:
        json.dump(organizations, f, indent=2, default=str)
    
    print(f"\n✅ Updated {updated_count} LA organizations with spread coordinates")
    
    # Verify the changes
    print(f"\nLA Organizations after update:")
    la_orgs = [org for org in organizations if org.get('city_category') == 'los_angeles']
    for org in la_orgs:
        print(f"  {org['name']}: {org.get('lat')}, {org.get('lng')} ({org.get('location_note', 'N/A')})")
        print(f"    Category: {org.get('category')}")
        print(f"    Funding: ${org.get('grant_amount_awarded', 0):,.0f}")
        print(f"    Mission: {org.get('mission', 'N/A')[:100]}...")
        print()

if __name__ == "__main__":
    spread_la_coordinates()
