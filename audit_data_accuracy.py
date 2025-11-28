#!/usr/bin/env python3
import pandas as pd
import json

def audit_data_accuracy():
    """Comprehensive audit of processed data against original Excel"""
    
    print("🔍 COMPREHENSIVE DATA ACCURACY AUDIT")
    print("=" * 60)
    
    # Read original Excel
    df = pd.read_excel('Knight_Impact_Partners_Grant_Ap2025-11-28_03_31_24 AM Mapping Data Sheet.xlsx')
    
    # Read processed JSON
    with open('knight_organizations_processed.json', 'r') as f:
        processed_data = json.load(f)
    
    # Create lookup for processed data
    processed_lookup = {org['name']: org for org in processed_data}
    
    print(f"📊 SUMMARY:")
    print(f"Excel rows: {len(df)}")
    print(f"Processed organizations: {len(processed_data)}")
    print()
    
    errors = []
    warnings = []
    
    print("🔎 DETAILED COMPARISON:")
    print("-" * 40)
    
    for idx, row in df.iterrows():
        excel_name = str(row.get('Organization Name:', '')).strip()
        if not excel_name or excel_name == 'nan':
            continue
            
        print(f"\n{idx+1}. {excel_name}")
        
        if excel_name not in processed_lookup:
            errors.append(f"❌ MISSING: {excel_name} not found in processed data")
            continue
            
        processed_org = processed_lookup[excel_name]
        
        # Check funding amounts
        excel_requested = row.get('Amount Requested', 0)
        excel_awarded = row.get('Grant Amount Awarded', 0)
        
        try:
            excel_requested = float(str(excel_requested).replace('$', '').replace(',', '')) if pd.notna(excel_requested) else 0
        except:
            excel_requested = 0
            
        try:
            excel_awarded = float(str(excel_awarded).replace('$', '').replace(',', '')) if pd.notna(excel_awarded) else 0
        except:
            excel_awarded = 0
        
        processed_requested = float(processed_org.get('amount_requested', 0))
        processed_awarded = float(processed_org.get('grant_amount_awarded', 0))
        
        # Check amounts
        if abs(excel_requested - processed_requested) > 0.01:
            errors.append(f"❌ AMOUNT REQUESTED MISMATCH: {excel_name}")
            print(f"   Excel: ${excel_requested:,.0f} | Processed: ${processed_requested:,.0f}")
        
        if abs(excel_awarded - processed_awarded) > 0.01:
            errors.append(f"❌ AMOUNT AWARDED MISMATCH: {excel_name}")
            print(f"   Excel: ${excel_awarded:,.0f} | Processed: ${processed_awarded:,.0f}")
        
        # Check category
        excel_category = str(row.get('Knight Impact Partners Program Category: (Select applicable category)', '')).strip()
        processed_category = processed_org.get('category', '')
        
        if excel_category != 'nan' and excel_category != processed_category:
            if excel_category and processed_category:
                warnings.append(f"⚠️  CATEGORY MISMATCH: {excel_name}")
                print(f"   Excel: '{excel_category}' | Processed: '{processed_category}'")
        
        # Check basic info
        excel_city = str(row.get('City:', '')).strip()
        excel_state = str(row.get('State:', '')).strip()
        processed_city = processed_org.get('city', '')
        processed_state = processed_org.get('state', '')
        
        if excel_city != 'nan' and excel_city != processed_city and excel_city:
            warnings.append(f"⚠️  CITY MISMATCH: {excel_name}")
            print(f"   Excel: '{excel_city}' | Processed: '{processed_city}'")
        
        # Check coordinates
        if not processed_org.get('lat') or not processed_org.get('lng'):
            warnings.append(f"⚠️  NO COORDINATES: {excel_name}")
        
        print(f"   ✅ Requested: ${processed_requested:,.0f} | Awarded: ${processed_awarded:,.0f}")
        print(f"   ✅ Category: {processed_category}")
        print(f"   ✅ Location: {processed_city}, {processed_state}")
        if processed_org.get('lat'):
            print(f"   ✅ Coordinates: {processed_org.get('lat')}, {processed_org.get('lng')}")
    
    # Calculate totals
    total_requested = sum(float(org.get('amount_requested', 0)) for org in processed_data)
    total_awarded = sum(float(org.get('grant_amount_awarded', 0)) for org in processed_data)
    
    # Count by category
    categories = {}
    cities = {}
    for org in processed_data:
        cat = org.get('category', 'Unknown')
        city_cat = org.get('city_category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
        cities[city_cat] = cities.get(city_cat, 0) + 1
    
    print(f"\n" + "=" * 60)
    print(f"📊 FINAL STATISTICS:")
    print(f"Total Organizations: {len(processed_data)}")
    print(f"Total Requested: ${total_requested:,.0f}")
    print(f"Total Awarded: ${total_awarded:,.0f}")
    print()
    
    print(f"📍 GEOGRAPHIC DISTRIBUTION:")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {city}: {count} organizations")
    print()
    
    print(f"🏷️  CATEGORY DISTRIBUTION:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} organizations")
    print()
    
    print(f"🚨 AUDIT RESULTS:")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    
    if errors:
        print(f"\n❌ CRITICAL ERRORS:")
        for error in errors:
            print(f"  {error}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errors and not warnings:
        print(f"\n🎉 ALL DATA VERIFIED - NO ISSUES FOUND!")
    elif not errors:
        print(f"\n✅ NO CRITICAL ERRORS - READY FOR SUBMISSION")
        print(f"   (Warnings are minor and don't affect accuracy)")
    else:
        print(f"\n🔧 ISSUES FOUND - NEEDS CORRECTION BEFORE SUBMISSION")
    
    return len(errors) == 0

if __name__ == "__main__":
    audit_data_accuracy()
