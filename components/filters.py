# components/filters.py

import streamlit as st
from config.settings import ALL_GRADES

def render_sidebar_filters(df_main):
    """
    Render sidebar filters dan return selected values
    Returns: dict dengan selected_brands, selected_cities, selected_users, selected_grades, start_date, end_date
    """
    st.sidebar.image("https://i0.wp.com/join.reddoorz.com/wp-content/uploads/2022/12/rdlogo.png?fit=960%2C434&ssl=1", width=200)
    st.sidebar.divider()
    st.sidebar.markdown("## 🔍 Filter Data")
    
    # Brand filter
    all_brands = sorted(df_main['BRAND_TYPE'].dropna().unique())
    selected_brands = st.sidebar.multiselect("Pilih Brand:", all_brands, default=all_brands)
    
    # City filter
    all_cities = sorted(df_main['CITY'].dropna().unique())
    selected_cities = st.sidebar.multiselect("Pilih Kota:", all_cities, default=all_cities)
    
    # User type filter
    all_users = sorted(df_main['USER_TYPE'].dropna().unique())
    selected_users = st.sidebar.multiselect("Pilih User Type:", all_users, default=all_users)
    
    # Grade filter (A-E only)
    selected_grades = st.sidebar.multiselect(
        "Filter Kualitas (Grade):",
        options=ALL_GRADES,
        default=ALL_GRADES
    )
    
    # Date filter
    min_date = df_main['CHECK_IN_DATE'].min()
    max_date = df_main['CHECK_IN_DATE'].max()
    
    start_date, end_date = st.sidebar.date_input(
        "Periode Check-In:",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    return {
        'selected_brands': selected_brands,
        'selected_cities': selected_cities,
        'selected_users': selected_users,
        'selected_grades': selected_grades,
        'start_date': start_date,
        'end_date': end_date
    }