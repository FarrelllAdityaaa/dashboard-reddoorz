# config/settings.py

# --- PAGE CONFIGURATION ---
PAGE_CONFIG = {
    "page_title": "RedDoorz Performance Dashboard",
    "page_icon": "🏨",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# --- COLOR PALETTES ---
color_map_brand = {
    'RedDoorz': '#8B0000',    # Merah Tua
    'RedPartner': '#FF9A8B',  # Merah Muda
    'Koolkost': '#FF7F50'     # Oranye Koral Terang
}

reddoorz_palette = [
    "#EB3638", # Bright Red
    "#C93333", # Medium Red
    "#A22B2B", # Dark Red
    "#8B1F2A", # Very Dark Red
    "#FF7F50", # Coral Orange
    "#FF9A8B", # Light Coral
    "#FFD1CF"  # Very Light Coral
]

city_color_map_fixed = {
    'Yogyakarta': '#5a5a5a',     # dark gray
    'Bandung':    '#d9d9d9',     # light gray
    'Jakarta':    '#FF7F50',     # Bright Coral Orange
    'Malang':     '#FF4500',     # orange-red
    'Surabaya':   '#9467bd'      # purple
}

# --- HELPER FUNCTIONS ---
def make_reddoorz_map(categories):
    """Generate color mapping untuk categories menggunakan reddoorz_palette"""
    cats = list(dict.fromkeys(categories))
    palette = reddoorz_palette
    mapping = {}
    for i, c in enumerate(cats):
        mapping[c] = palette[i % len(palette)]
    return mapping

# --- DATA CONSTANTS ---
REQUIRED_COLUMNS = {
    'bookings': ['BOOKING_ID','USER_ID','PROPERTY_CODE','CHECK_IN_DATE','ROOM_NIGHTS','REVENUE_DOLLAR','USER_TYPE'],
    'property': ['PROPERTY_CODE','BRAND_TYPE','CITY','INVENTORY','COHORT_DATE'],
    'user': ['USER_ID','USER_TYPE','USER_GENDER']
}

DATA_PATHS = {
    'bookings': 'data/Online Budget Hotel Dataset.xlsx - Bookings Table.csv',
    'property': 'data/Online Budget Hotel Dataset.xlsx - Property Table.csv',
    'user': 'data/Online Budget Hotel Dataset.xlsx - User Table.csv'
}

ALL_GRADES = ['A', 'B', 'C', 'D', 'E']