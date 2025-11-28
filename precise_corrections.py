#!/usr/bin/env python3
import pandas as pd
import json

def make_precise_corrections():
    """Make precise corrections based on Excel row positions"""
    
    # Read Excel
    df = pd.read_excel('Knight_Impact_Partners_Grant_Ap2025-11-28_03_31_24 AM Mapping Data Sheet.xlsx')
    
    # Read processed JSON
    with open('knight_organizations_processed.json', 'r') as f:
        organizations = json.load(f)
    
    print("🔧 MAKING PRECISE CORRECTIONS")
    print("=" * 50)
    
    corrections = 0
    
    # Process each row and match to corresponding organization in JSON
    for idx, row in df.iterrows():
        excel_name = str(row.get('Organization Name:', '')).strip()
        if not excel_name or excel_name == 'nan':
            continue
            
        # Get Excel amounts
        excel_awarded = row.get('Grant Amount Awarded', 0)
        try:
            excel_awarded = float(str(excel_awarded).replace('$', '').replace(',', '')) if pd.notna(excel_awarded) else 0
        except:
            excel_awarded = 0
        
        # Find corresponding organization in JSON (they should be in same order)
        if idx < len(organizations):
            org = organizations[idx]
            
            # Verify this is the right organization
            if org['name'] == excel_name:
                current_awarded = float(org.get('grant_amount_awarded', 0))
                
                # Special case: Greater Auburn Gresham should be $150K (user correction)
                if 'Greater Auburn Gresham' in excel_name:
                    if current_awarded != 150000:
                        print(f"✅ {excel_name}: ${current_awarded:,.0f} → $150,000 (user correction)")
                        org['grant_amount_awarded'] = 150000.0
                        corrections += 1
                    continue
                
                # For all others, match Excel exactly
                if abs(excel_awarded - current_awarded) > 0.01:
                    print(f"✅ {excel_name}: ${current_awarded:,.0f} → ${excel_awarded:,.0f}")
                    org['grant_amount_awarded'] = excel_awarded
                    corrections += 1
            else:
                print(f"⚠️  Order mismatch at row {idx+1}: Excel='{excel_name}' vs JSON='{org['name']}'")
    
    # Save corrected data
    with open('knight_organizations_processed.json', 'w') as f:
        json.dump(organizations, f, indent=2, default=str)
    
    print(f"\n✅ CORRECTIONS COMPLETED: {corrections} changes made")
    
    # Calculate final totals
    total_awarded = sum(float(org.get('grant_amount_awarded', 0)) for org in organizations)
    total_requested = sum(float(org.get('amount_requested', 0)) for org in organizations)
    
    print(f"\n📊 FINAL TOTALS:")
    print(f"Total Requested: ${total_requested:,.0f}")
    print(f"Total Awarded: ${total_awarded:,.0f}")
    
    return corrections

if __name__ == "__main__":
    make_precise_corrections()
