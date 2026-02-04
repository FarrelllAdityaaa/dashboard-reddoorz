# tabs/tab_region_revenue.py

import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import city_color_map_fixed, reddoorz_palette

def render_tab(filtered_df, prop_final):
    """Render Tab 2: Wilayah & Revenue"""
    
    st.subheader("Q3: Peringkat Kota Berdasarkan Revenue")
    
    city_agg = filtered_df.groupby('CITY').agg(
        TOTAL_REVENUE=('REVENUE_DOLLAR','sum'),
        TOTAL_SOLD=('ROOM_NIGHTS','sum')
    ).reset_index()

    # City-level available
    city_available = prop_final.groupby('CITY')['AVAILABLE'].sum().reset_index().rename(columns={'AVAILABLE':'CITY_AVAILABLE'})

    # Merge
    df_city = pd.merge(city_agg, city_available, on='CITY', how='left')
    df_city['CITY_AVAILABLE'] = df_city['CITY_AVAILABLE'].fillna(0)

    # Calculate metrics
    df_city['ADR'] = df_city.apply(lambda r: (r['TOTAL_REVENUE']/r['TOTAL_SOLD']) if r['TOTAL_SOLD'] and r['TOTAL_SOLD']>0 else 0, axis=1)
    df_city['OCC_RATE'] = df_city.apply(lambda r: (r['TOTAL_SOLD'] / r['CITY_AVAILABLE']) if r['CITY_AVAILABLE']>0 else 0, axis=1)
    df_city['OCCUPANCY'] = df_city['OCC_RATE'] * 100
    df_city['REVPAR'] = df_city['ADR'] * df_city['OCC_RATE']

    df_city_sorted = df_city.sort_values('TOTAL_REVENUE', ascending=False)
    df_city_sorted['K_format'] = (df_city_sorted['TOTAL_REVENUE'] / 1000).round().astype(int).astype(str) + "k"

    # Color mapping
    cities_present = df_city_sorted['CITY'].unique().tolist()
    city_color_map_dynamic = {}
    palette_idx = 0
    for c in cities_present:
        if c in city_color_map_fixed:
            city_color_map_dynamic[c] = city_color_map_fixed[c]
        else:
            city_color_map_dynamic[c] = reddoorz_palette[palette_idx % len(reddoorz_palette)]
            palette_idx += 1

    fig_q3 = px.bar(
        df_city_sorted, x="CITY", y="TOTAL_REVENUE",
        color="CITY", color_discrete_map=city_color_map_dynamic,
        text="K_format",
        labels={'TOTAL_REVENUE':'Total Revenue ($)','CITY':'Kota'},
        hover_data={'TOTAL_REVENUE':':,.0f','ADR':':.2f','OCCUPANCY':':.2f','CITY_AVAILABLE':True,'CITY':False}
    )

    fig_q3.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0.25)", marker_line_width=1.2)
    fig_q3.update_layout(
        xaxis={'categoryorder':'total descending'}, 
        bargap=0.22, 
        hoverlabel=dict(bgcolor="white",font_color="black"), 
        legend_title_text='Kota', 
        margin=dict(t=40,b=40,l=40,r=20), 
        yaxis_tickformat='.0s'
    )
    st.plotly_chart(fig_q3, use_container_width=True)

    st.markdown("**Tabel ringkasan per-kota (Total Revenue, ADR, Okupansi, dan RevPAR)**")
    st.dataframe(
        df_city_sorted[['CITY','TOTAL_REVENUE','ADR','OCCUPANCY','REVPAR']]
        .sort_values('TOTAL_REVENUE', ascending=False)
        .style.format({'TOTAL_REVENUE':'{:.0f}','ADR':'{:.2f}','OCCUPANCY':'{:.2f}','REVPAR':'{:.2f}'})
    )

    # Insight Q3
    st.info("""
    **Temuan Kritis**: **Yogyakarta** adalah mesin revenue utama (**\$427K**) yang didorong oleh **Okupansi tertinggi** (1.61%). **ADR Seragam** (sekitar **\$5.00**) di semua kota menunjukkan pendapatan TIDAK didorong harga. Seluruh pasar menderita krisis volume yang parah (RevPAR sangat rendah).
    **Rekomendasi Strategi**: 1) **Monetisasi Yogyakarta/Jakarta**: Segera uji ADR naik **\$0.50** di properti Grade C/D di Yogyakarta dan Jakarta, karena permintaan volume terbukti ada. 2) **Fokus Volume**: Alokasikan *marketing* agresif untuk meningkatkan Okupansi di **Bandung, Malang, dan Surabaya** (pasar yang tertinggal).
    """)