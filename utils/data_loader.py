# utils/data_loader.py

import streamlit as st
import pandas as pd
from config.settings import DATA_PATHS, REQUIRED_COLUMNS

@st.cache_data
def load_data():
    """Load dan preprocess semua dataset"""
    try:
        # Load datasets
        df_bookings = pd.read_csv(DATA_PATHS['bookings'])
        df_property = pd.read_csv(DATA_PATHS['property'])
        df_user = pd.read_csv(DATA_PATHS['user'])
        
        # Drop Unnamed columns
        for df in [df_bookings, df_property, df_user]:
            df.drop(columns=[col for col in df.columns if 'Unnamed' in col], inplace=True, errors='ignore')
        
        # Convert data types - dates
        df_bookings['CHECK_IN_DATE'] = pd.to_datetime(df_bookings['CHECK_IN_DATE'], errors='coerce')
        df_property['COHORT_DATE'] = pd.to_datetime(df_property['COHORT_DATE'], errors='coerce')
        
        # Convert data types - numerics
        df_bookings['REVENUE_DOLLAR'] = pd.to_numeric(df_bookings['REVENUE_DOLLAR'], errors='coerce')
        df_bookings['ROOM_NIGHTS'] = pd.to_numeric(df_bookings['ROOM_NIGHTS'], errors='coerce')
        df_property['INVENTORY'] = pd.to_numeric(df_property['INVENTORY'], errors='coerce')
        
        # Standardize text columns
        if 'USER_TYPE' in df_bookings.columns:
            df_bookings['USER_TYPE'] = df_bookings['USER_TYPE'].astype(str).str.strip().str.title()
        if 'USER_TYPE' in df_user.columns:
            df_user['USER_TYPE'] = df_user['USER_TYPE'].astype(str).str.strip().str.title()
        if 'BRAND_TYPE' in df_property.columns:
            df_property['BRAND_TYPE'] = df_property['BRAND_TYPE'].astype(str).str.strip().str.title()
        if 'CITY' in df_property.columns:
            df_property['CITY'] = df_property['CITY'].astype(str).str.strip().str.title()
        
        # Merge datasets
        df_merged = pd.merge(
            df_bookings,
            df_property[['PROPERTY_CODE', 'BRAND_TYPE', 'CITY', 'INVENTORY']],
            on='PROPERTY_CODE',
            how='left'
        )
        
        df_merged_user = pd.merge(
            df_merged,
            df_user[['USER_ID', 'USER_TYPE', 'USER_GENDER']],
            on='USER_ID',
            how='left'
        )
        
        return df_merged_user, df_property
        
    except FileNotFoundError:
        return None, None

def validate_columns(df_main, df_property):
    """Validate required columns exist"""
    missing = []
    
    for c in REQUIRED_COLUMNS['bookings']:
        if c not in df_main.columns:
            missing.append(c)
    
    for c in REQUIRED_COLUMNS['property']:
        if c not in df_property.columns:
            missing.append(c)
    
    return missing