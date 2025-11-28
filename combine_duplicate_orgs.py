#!/usr/bin/env python3
import json

def combine_duplicate_organizations():
    """Combine organizations with multiple grants into single entries"""
    
    # Load data
    with open('knight_organizations_processed.json', 'r') as f:
        data = json.load(f)
    
    print('🔄 COMBINING ORGANIZATIONS WITH MULTIPLE GRANTS')
    print('=' * 60)
    
    # Group by organization name
    org_groups = {}
    for org in data:
        name = org['name']
        if name not in org_groups:
            org_groups[name] = []
        org_groups[name].append(org)
    
    # Create combined data
    combined_data = []
    
    for name, orgs in org_groups.items():
        if len(orgs) == 1:
            # Single grant - keep as is
            combined_data.append(orgs[0])
        else:
            # Multiple grants - combine into one entry
            print(f'\n📝 {name}: {len(orgs)} grants')
            
            # Use first entry as base
            combined_org = orgs[0].copy()
            
            # Combine grants into an array
            grants = []
            total_awarded = 0
            total_requested = 0
            
            for i, org in enumerate(orgs, 1):
                grant_awarded = float(org.get('grant_amount_awarded', 0))
                grant_requested = float(org.get('amount_requested', 0))
                category = org.get('category', 'Not specified')
                grant_type = org.get('grant_type', 'Not specified')
                
                grants.append({
                    'number': i,
                    'amount_awarded': grant_awarded,
                    'amount_requested': grant_requested,
                    'category': category,
                    'grant_type': grant_type
                })
                
                total_awarded += grant_awarded
                total_requested += grant_requested
                
                print(f'  Grant {i}: \${grant_awarded:,.0f} - {category}')
            
            # Update combined entry
            combined_org['grants'] = grants
            combined_org['grant_amount_awarded'] = total_awarded
            combined_org['amount_requested'] = total_requested
            combined_org['has_multiple_grants'] = True
            combined_org['grant_count'] = len(grants)
            
            print(f'  Combined Total: \${total_awarded:,.0f}')
            
            combined_data.append(combined_org)
    
    # Save combined data
    with open('knight_organizations_combined.json', 'w') as f:
        json.dump(combined_data, f, indent=2, default=str)
    
    print(f'\n✅ COMBINATION COMPLETE')
    print(f'Original entries: {len(data)}')
    print(f'Combined entries: {len(combined_data)}')
    print(f'Reduced by: {len(data) - len(combined_data)} duplicate markers')
    
    # Show new totals
    total_awarded = sum(float(org.get('grant_amount_awarded', 0)) for org in combined_data)
    print(f'\nTotal funding (combined): \${total_awarded:,.0f}')
    
    return combined_data

if __name__ == "__main__":
    combine_duplicate_organizations()
