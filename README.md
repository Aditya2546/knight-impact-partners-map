# Knight Impact Partners - Interactive Map

A clean, interactive map displaying Knight Impact Partners' grantee organizations across Chicago, Evanston, and Los Angeles.

## 🗺️ **Features**

- **Interactive Organization Markers**: Click to view detailed information about each organization
- **Smart Filtering**: Filter by individual organization, city, or category
- **Real-time Statistics**: View total organizations and funding amounts
- **Color-coded Categories**: Visual distinction between different program areas
- **Responsive Design**: Works on desktop and mobile devices

## 📊 **Data Overview**

- **71 Organizations** across multiple cities
- **$21.9M+ in Total Funding** awarded
- **9 Program Categories** including Human Services, Community Development, Education, and Health
- **Primary Coverage**: Chicago (46 orgs), plus Evanston and other locations

## 🎨 **Program Categories**

- **Human Services** (30 orgs) - Blue markers
- **Community Development** (10 orgs) - Green markers  
- **Education** (7 orgs) - Orange markers
- **Health** (6 orgs) - Red markers
- **Health and Human Services** (5 orgs) - Purple markers
- **Systems Building** (5 orgs) - Cyan markers
- **Community Building** (5 orgs) - Lime markers

## 🚀 **Usage**

### Local Development
```bash
# Start local server
python3 -m http.server 8002

# View map
open http://localhost:8002/knight_simple_map.html
```

### Data Processing
```bash
# Process Excel data (if updating)
python3 process_knight_data.py
```

## 📁 **Files**

- `knight_simple_map.html` - Main interactive map
- `knight_organizations_processed.json` - Processed organization data
- `process_knight_data.py` - Data processing script
- `Knight_Impact_Partners_Grant_Ap2025-11-28_03_31_24 AM Mapping Data Sheet.xlsx` - Source data

## 🔧 **Technical Details**

- **Mapping**: Leaflet.js for interactive maps
- **Geocoding**: Geopy for address-to-coordinate conversion
- **Data Processing**: Python with Pandas for Excel processing
- **Styling**: Modern dark theme with Inter font
- **No Dependencies**: Pure HTML/CSS/JS for easy deployment

## 📈 **Statistics**

- Total Organizations: 71
- Total Funding Awarded: $21,930,499
- Cities Covered: Chicago, Evanston, Round Lake Park
- Categories: 9 distinct program areas

---

**Built for Knight Impact Partners** | Last Updated: November 2025
