# utils/calculations.py

import pandas as pd

def get_grade_logic(occupancy_pct):
    """Tentukan grade berdasarkan occupancy percentage"""
    if occupancy_pct > 80:
        return 'A'
    elif occupancy_pct >= 70:
        return 'B'
    elif occupancy_pct >= 40:
        return 'C'
    elif occupancy_pct >= 20:
        return 'D'
    else:
        return 'E'

def calculate_grades(df_main, df_property, start_date, end_date, selected_brands, selected_cities):
    """
    Calculate property grades berdasarkan occupancy rate
    Returns: prop_final (DataFrame dengan grade per property)
    """
    # Filter transaksi dalam rentang tanggal
    temp_df = df_main[
        (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) & 
        (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
    ]
    
    # Hitung total SOLD per property
    prop_agg = temp_df.groupby('PROPERTY_CODE').agg(
        SOLD=('ROOM_NIGHTS', 'sum')
    ).reset_index()
    
    # Property master
    active_props_all = df_property[['PROPERTY_CODE','BRAND_TYPE','CITY','INVENTORY','COHORT_DATE']].copy()
    active_props_all['COHORT_DATE'] = pd.to_datetime(active_props_all['COHORT_DATE'], errors='coerce')
    
    # Merge dengan sold
    prop_final = pd.merge(active_props_all, prop_agg, on='PROPERTY_CODE', how='left').fillna({'SOLD':0})
    
    # Hitung ACTIVE_DAYS per property
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    prop_final['COHORT_DATE'] = prop_final['COHORT_DATE'].fillna(start_dt)
    prop_final['ACTIVE_START'] = prop_final['COHORT_DATE'].apply(lambda d: d if d > start_dt else start_dt)
    prop_final['ACTIVE_END'] = end_dt
    prop_final['ACTIVE_DAYS'] = (prop_final['ACTIVE_END'] - prop_final['ACTIVE_START']).dt.days + 1
    prop_final.loc[prop_final['ACTIVE_DAYS'] < 0, 'ACTIVE_DAYS'] = 0
    prop_final['ACTIVE_DAYS'] = prop_final['ACTIVE_DAYS'].fillna(0).astype(int)
    
    # Hitung AVAILABLE
    prop_final['INVENTORY'] = pd.to_numeric(prop_final['INVENTORY'], errors='coerce').fillna(0).astype(float)
    prop_final['AVAILABLE'] = prop_final['INVENTORY'] * prop_final['ACTIVE_DAYS']
    
    # Compute occupancy %
    prop_final['OCC'] = 0.0
    mask = prop_final['AVAILABLE'] > 0
    prop_final.loc[mask, 'OCC'] = (prop_final.loc[mask, 'SOLD'] / prop_final.loc[mask, 'AVAILABLE']) * 100
    
    # Tentukan GRADE
    prop_final['GRADE'] = prop_final['OCC'].apply(get_grade_logic)
    
    return prop_final

def calculate_kpis(filtered_df):
    """
    Calculate KPI metrics dari filtered dataframe
    Returns: dict dengan total_revenue, total_bookings, total_nights, avg_adr, retention_rate
    """
    total_revenue = filtered_df['REVENUE_DOLLAR'].sum()
    total_bookings = filtered_df['BOOKING_ID'].nunique()
    total_nights = filtered_df['ROOM_NIGHTS'].sum()
    avg_adr = total_revenue / total_nights if total_nights > 0 else 0
    
    repeat_user_count = filtered_df[filtered_df['USER_TYPE'].str.lower() == 'repeat user']['USER_ID'].nunique()
    total_unique_users = filtered_df['USER_ID'].nunique()
    retention_rate = (repeat_user_count / total_unique_users * 100) if total_unique_users > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'total_nights': total_nights,
        'avg_adr': avg_adr,
        'retention_rate': retention_rate,
        'repeat_user_count': repeat_user_count,
        'total_unique_users': total_unique_users
    }

def format_revenue_display(revenue):
    """Format revenue untuk display (M/K notation)"""
    if revenue >= 1_000_000:
        return f"${revenue/1_000_000:.2f} M"
    elif revenue >= 1_000:
        return f"${revenue/1_000:.2f} K"
    else:
        return f"${revenue:,.2f}"