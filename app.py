import streamlit as st
import pandas as pd
import warnings

# Import configurations
from config.settings import PAGE_CONFIG
from config.styles import apply_all_styles

# Import utilities
from utils.data_loader import load_data, validate_columns
from utils.calculations import calculate_grades, calculate_kpis

# Import components
from components.filters import render_sidebar_filters
from components.header import render_title, render_business_context, render_kpi_cards
from components.footer import render_footer

# Import tabs
from tabs import tab_asset_quality, tab_region_revenue, tab_customer_loyalty, tab_summary

# --- KONFIGURASI HALAMAN ---
st.set_page_config(**PAGE_CONFIG)

# Matikan warning
warnings.filterwarnings('ignore')

# Apply all styles
apply_all_styles()

# --- LOAD DATA ---
df_main, df_prop_raw = load_data()

if df_main is None:
    st.error("❌ File CSV tidak ditemukan. Pastikan 3 file dataset ada di folder 'data/'")
    st.stop()

# --- VALIDATE COLUMNS ---
missing = validate_columns(df_main, df_prop_raw)
if missing:
    st.error(f"Kolom wajib hilang: {missing}. Periksa file sumber.")
    st.stop()

# --- SIDEBAR FILTERS ---
filters = render_sidebar_filters(df_main)

# Extract filter values
selected_brands = filters['selected_brands']
selected_cities = filters['selected_cities']
selected_users = filters['selected_users']
selected_grades = filters['selected_grades']
start_date = filters['start_date']
end_date = filters['end_date']

# --- CALCULATE GRADES ---
prop_final = calculate_grades(
    df_main, 
    df_prop_raw, 
    start_date, 
    end_date, 
    selected_brands, 
    selected_cities
)

# Map grades back to main dataframe
grade_mapping = dict(zip(prop_final['PROPERTY_CODE'], prop_final['GRADE']))
df_main['CURRENT_GRADE'] = df_main['PROPERTY_CODE'].map(grade_mapping).fillna('Unknown')

# --- APPLY ALL FILTERS ---
filtered_df = df_main[
    (df_main['BRAND_TYPE'].isin(selected_brands)) &
    (df_main['CITY'].isin(selected_cities)) &
    (df_main['USER_TYPE'].isin(selected_users)) &
    (df_main['CURRENT_GRADE'].isin(selected_grades)) &
    (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) &
    (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
].copy()

# Filter prop_final for grade distribution
pf_filtered = prop_final[
    (prop_final['BRAND_TYPE'].isin(selected_brands)) &
    (prop_final['CITY'].isin(selected_cities)) &
    (prop_final['GRADE'].isin(selected_grades))
].copy()

# Warning for invalid inventory
if (prop_final['INVENTORY'] <= 0).any():
    st.warning("Beberapa properti memiliki INVENTORY <= 0. Hasil okupansi/proporsi bisa tidak valid untuk property tersebut.")

# --- HEADER: TITLE & BUSINESS CONTEXT ---
render_title(start_date, end_date)
render_business_context()

# --- KPI CARDS ---
kpis = calculate_kpis(filtered_df)
render_kpi_cards(kpis)

st.divider()

# --- TABS ANALISIS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Aset & Kualitas", 
    "2. Wilayah & Revenue", 
    "3. Pelanggan & Loyalitas", 
    "4. Rangkuman Aksi Strategis"
])

with tab1:
    tab_asset_quality.render_tab(pf_filtered, df_prop_raw, selected_brands)

with tab2:
    tab_region_revenue.render_tab(filtered_df, prop_final)

with tab3:
    tab_customer_loyalty.render_tab(filtered_df)

with tab4:
    tab_summary.render_tab()

# --- FOOTER ---
render_footer()