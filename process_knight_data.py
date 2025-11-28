#!/usr/bin/env python3
import pandas as pd
import json
import re
from geopy.geocoders import Nominatim
import time

def clean_text(text):
    """Clean and normalize text data"""
    if pd.isna(text):
        return ""
    return str(text).strip()

def parse_funding(funding_str):
    """Parse funding amount from string"""
    if pd.isna(funding_str):
        return 0
    
    # Convert to string and clean
    funding_str = str(funding_str).strip()
    
    # Remove currency symbols and commas
    funding_str = re.sub(r'[$,]', '', funding_str)
    
    # Try to extract number
    try:
        return float(funding_str)
    except:
        return 0

def geocode_address(address, city, state=""):
    """Geocode address to get lat/lng"""
    geolocator = Nominatim(user_agent="knight_impact_mapper")
    
    try:
        # Construct full address
        full_address = f"{address}, {city}"
        if state:
            full_address += f", {state}"
        
        location = geolocator.geocode(full_address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            # Try just city if full address fails
            location = geolocator.geocode(f"{city}, USA", timeout=10)
            if location:
                return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
    
    return None, None

def process_knight_data():
    """Process the Knight Impact Partners Excel file"""
    
    file_path = "Knight_Impact_Partners_Grant_Ap2025-11-28_03_31_24 AM Mapping Data Sheet.xlsx"
    
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        print(f"Successfully read Excel file with {len(df)} rows")
        
        organizations = []
        
        for idx, row in df.iterrows():
            # Skip rows without organization names
            org_name = clean_text(row.get('Organization Name:', ''))
            if not org_name:
                continue
                
            print(f"Processing: {org_name}")
            
            # Extract basic info
            org_data = {
                'id': str(idx + 1),
                'name': org_name,
                'address': clean_text(row.get('Address (Line 1):', '')),
                'address_line2': clean_text(row.get('Address (Line 2):', '')),
                'city': clean_text(row.get('City:', '')),
                'state': clean_text(row.get('State:', '')),
                'postal_code': clean_text(row.get('Postal Code:', '')),
                'website': clean_text(row.get('Website:', '')),
                'email': clean_text(row.get('Email:', '')),
                'phone': clean_text(row.get('Phone Number:', '')),
                'year_founded': clean_text(row.get('Year Founded:', '')),
                'tax_id': clean_text(row.get('Tax ID:', '')),
            }
            
            # Contact info
            org_data['contact_first_name'] = clean_text(row.get('First Name:', ''))
            org_data['contact_last_name'] = clean_text(row.get('Last Name:', ''))
            org_data['contact_title'] = clean_text(row.get('Title:', ''))
            org_data['contact_email'] = clean_text(row.get('Email Address:', ''))
            
            # Leadership info
            org_data['leader_first_name'] = clean_text(row.get('First Name:.1', ''))
            org_data['leader_last_name'] = clean_text(row.get('Last Name:.1', ''))
            org_data['leader_title'] = clean_text(row.get('Title:.1', ''))
            org_data['leader_email'] = clean_text(row.get('Email Address:.1', ''))
            
            # Staffing
            org_data['full_time_staff'] = clean_text(row.get('# of Paid Full Time Staff:', ''))
            org_data['part_time_staff'] = clean_text(row.get('# of Paid Part Time Staff:', ''))
            org_data['volunteers'] = clean_text(row.get('# of Volunteers:', ''))
            
            # Mission and program info
            org_data['mission'] = clean_text(row.get('Organization Mission & Vision Statements:', ''))
            org_data['program_name'] = clean_text(row.get('1. Program Name/Title (or N/A): ', ''))
            org_data['program_description'] = clean_text(row.get('2. Description of Your Organization/Program: Describe the primary focus, target population, key activities and organizational goals', ''))
            
            # Grant info
            org_data['amount_requested'] = parse_funding(row.get('Amount Requested', 0))
            org_data['grant_amount_awarded'] = parse_funding(row.get('Grant Amount Awarded', 0))
            org_data['grant_type'] = clean_text(row.get('Grant Type', ''))
            org_data['category'] = clean_text(row.get('Knight Impact Partners Program Category: (Select applicable category)', ''))
            
            # Demographics and target population
            org_data['age_groups'] = clean_text(row.get('Age:', ''))
            org_data['target_age_group'] = clean_text(row.get('What is your primary target age group?', ''))
            org_data['race_ethnicity'] = clean_text(row.get('Race / Ethnicity - Check all applicable groups that represent a significant (approx. 20% or more) portion of the population served by your organization.', ''))
            org_data['gender_identity'] = clean_text(row.get('Gender Identity - Check all applicable groups that represent a significant (approx. 20% or more) portion of the population served by your organization.', ''))
            org_data['low_income_percentage'] = clean_text(row.get('Low Income % of constituents', ''))
            
            # Neighborhood info
            org_data['neighborhoods'] = clean_text(row.get('Please list the specific primary Chicago neighborhoods/communities where the organization does at least 10% of its work', ''))
            org_data['primary_neighborhood'] = clean_text(row.get('Neighborhood', ''))
            org_data['secondary_neighborhood'] = clean_text(row.get('Neighborhood 2', ''))
            
            # Financial info
            org_data['public_private_split'] = clean_text(row.get('What percentage of your current total organizational budget is public versus private?', ''))
            org_data['private_funding_sources'] = clean_text(row.get('Top Three Existing and Anticipated Private Funding Sources', ''))
            org_data['public_funding_sources'] = clean_text(row.get('Top Three Existing and Anticipated Public Funding Sources', ''))
            
            # Determine city category for filtering
            city_name = org_data['city'].lower()
            if 'chicago' in city_name or org_data['state'].lower() in ['il', 'illinois']:
                org_data['city_category'] = 'chicago'
            elif any(la_term in city_name for la_term in ['los angeles', 'la', 'angeles']):
                org_data['city_category'] = 'los_angeles'
            else:
                org_data['city_category'] = 'other'
            
            # Create full address for geocoding
            full_address = org_data['address']
            if org_data['address_line2']:
                full_address += f", {org_data['address_line2']}"
            
            # Geocode if we have address info
            if full_address and org_data['city']:
                print(f"  Geocoding: {full_address}, {org_data['city']}")
                lat, lng = geocode_address(full_address, org_data['city'], org_data['state'])
                org_data['lat'] = lat
                org_data['lng'] = lng
                time.sleep(0.2)  # Be respectful to geocoding service
            
            organizations.append(org_data)
        
        # Save processed data
        with open('knight_organizations_processed.json', 'w') as f:
            json.dump(organizations, f, indent=2, default=str)
        
        print(f"\nProcessed {len(organizations)} organizations")
        print("Data saved to knight_organizations_processed.json")
        
        # Print summary statistics
        cities = {}
        categories = {}
        total_requested = 0
        total_awarded = 0
        
        for org in organizations:
            city = org.get('city', 'Unknown')
            category = org.get('category', 'Unknown')
            requested = org.get('amount_requested', 0)
            awarded = org.get('grant_amount_awarded', 0)
            
            cities[city] = cities.get(city, 0) + 1
            categories[category] = categories.get(category, 0) + 1
            total_requested += requested
            total_awarded += awarded
        
        print(f"\nSummary:")
        print(f"Total Organizations: {len(organizations)}")
        print(f"Total Amount Requested: ${total_requested:,.2f}")
        print(f"Total Amount Awarded: ${total_awarded:,.2f}")
        print(f"\nCities: {dict(sorted(cities.items(), key=lambda x: x[1], reverse=True))}")
        print(f"\nCategories: {dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))}")
        
        return organizations
        
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    process_knight_data()
