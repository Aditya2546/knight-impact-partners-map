#!/usr/bin/env python3
import pandas as pd
import json

def fix_funding_discrepancies():
    """Fix all funding amount discrepancies found in audit"""
    
    # Read original Excel
    df = pd.read_excel('Knight_Impact_Partners_Grant_Ap2025-11-28_03_31_24 AM Mapping Data Sheet.xlsx')
    
    # Read processed JSON
    with open('knight_organizations_processed.json', 'r') as f:
        organizations = json.load(f)
    
    # Create lookup for processed data
    processed_lookup = {org['name']: org for org in organizations}
    
    corrections_made = []
    
    print("🔧 FIXING FUNDING DISCREPANCIES")
    print("=" * 50)
    
    for idx, row in df.iterrows():
        excel_name = str(row.get('Organization Name:', '')).strip()
        if not excel_name or excel_name == 'nan':
            continue
            
        if excel_name not in processed_lookup:
            continue
            
        processed_org = processed_lookup[excel_name]
        
        # Get Excel amounts
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
        
        # Fix mismatches
        requested_mismatch = abs(excel_requested - processed_requested) > 0.01
        awarded_mismatch = abs(excel_awarded - processed_awarded) > 0.01
        
        if requested_mismatch or awarded_mismatch:
            print(f"\n📝 {excel_name}:")
            
            if requested_mismatch:
                print(f"   Requested: {processed_requested:,.0f} → {excel_requested:,.0f}")
                processed_org['amount_requested'] = excel_requested
                
            if awarded_mismatch:
                print(f"   Awarded: {processed_awarded:,.0f} → {excel_awarded:,.0f}")
                processed_org['grant_amount_awarded'] = excel_awarded
                
            corrections_made.append(excel_name)
    
    # Save corrected data
    with open('knight_organizations_processed.json', 'w') as f:
        json.dump(organizations, f, indent=2, default=str)
    
    print(f"\n✅ CORRECTIONS COMPLETED")
    print(f"Organizations corrected: {len(corrections_made)}")
    
    # Calculate new totals
    total_requested = sum(float(org.get('amount_requested', 0)) for org in organizations)
    total_awarded = sum(float(org.get('grant_amount_awarded', 0)) for org in organizations)
    
    print(f"\n📊 NEW TOTALS:")
    print(f"Total Requested: ${total_requested:,.0f}")
    print(f"Total Awarded: ${total_awarded:,.0f}")
    
    return corrections_made

if __name__ == "__main__":
    fix_funding_discrepancies()
