# tabs/tab_asset_quality.py

import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import make_reddoorz_map, color_map_brand, reddoorz_palette

def render_tab(prop_final, df_property, selected_brands):
    """Render Tab 1: Aset & Kualitas"""
    
    st.subheader("Q1: Komposisi Performa Okupansi Properti (Grade A-E)")
    
    grade_dist = prop_final['GRADE'].value_counts().reset_index()
    grade_dist.columns = ['GRADE','COUNT']
    grade_dist = grade_dist.sort_values('GRADE', key=lambda s: s.map({'A':0,'B':1,'C':2,'D':3,'E':4}))

    # Use reddoorz palette for grade slices
    reddoorz_grade_map = make_reddoorz_map(['A','B','C','D','E'])

    st.markdown("<div class='chart-hover'>", unsafe_allow_html=True)

    # Calculate percentages for pull logic
    total = grade_dist['COUNT'].sum() if grade_dist['COUNT'].sum() > 0 else 1
    grade_dist['PCT'] = grade_dist['COUNT'] / total

    pulls = []
    for pct in grade_dist['PCT']:
        if pct < 0.06:
            pulls.append(0.20)
        elif pct < 0.12:
            pulls.append(0.10)
        else:
            pulls.append(0.0)

    fig_q1 = px.pie(
        grade_dist, names='GRADE', values='COUNT',
        color='GRADE', color_discrete_map=reddoorz_grade_map,
        hole=0.35,
        category_orders={'GRADE': ['A','B','C','D','E']}
    )

    fig_q1.update_traces(
        textposition='outside',
        textinfo='percent+label',
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        pull=pulls,
        marker=dict(line=dict(color='white', width=1)),
        textfont=dict(size=12),
        automargin=True
    )

    fig_q1.update_layout(
        margin=dict(t=10, b=160, l=40, r=140),
        height=520,
        autosize=True,
        showlegend=True,
        legend=dict(orientation="v", y=0.55, x=0.02, title="Grade", font=dict(size=11))
    )

    st.plotly_chart(fig_q1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Brand breakdown
    brand_counts = prop_final.groupby('BRAND_TYPE')['PROPERTY_CODE'].nunique().rename('TOTAL_PROPERTY')
    grade_e_counts = prop_final[prop_final['GRADE']=='E'].groupby('BRAND_TYPE')['PROPERTY_CODE'].nunique().rename('E_COUNT')
    brand_summary = pd.concat([brand_counts, grade_e_counts], axis=1).fillna(0)
    brand_summary['E_PROP'] = brand_summary['E_COUNT'] / brand_summary['TOTAL_PROPERTY']
    brand_summary = brand_summary.sort_values('E_PROP', ascending=False).reset_index()

    st.markdown("**Brand breakdown (proporsi Grade E)**")
    st.dataframe(brand_summary.style.format({'E_PROP':'{:.1%}','TOTAL_PROPERTY':'{:.0f}','E_COUNT':'{:.0f}'}))

    # Insight Q1
    st.info("""
    **Temuan Kritis**: $\mathbf{95.4\%}$ aset berada di **Grade E** (<20% Okupansi), krisis merata di semua brand. Properti unggul (A/B) hanya 0.8%. **RedPartner** ($\mathbf{95.8\%}$) memiliki proporsi E tertinggi.
    **Rekomendasi Strategi**: 1) **Delisting** agresif pada Grade E terburuk (fokus RedPartner). 2) **Fokus perbaikan** intensif hanya pada Grade C/D ($\sim 4\%$) untuk peningkatan cepat. 3) **Kloning** praktik operasional dari 3 properti Grade A.
    """)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Q4: Tren Akuisisi
    st.subheader("Q4: Tren Akuisisi Properti Baru (Tahunan)")
    df_cohort = df_property[df_property['BRAND_TYPE'].isin(selected_brands)].copy()
    df_cohort['YEAR'] = df_cohort['COHORT_DATE'].dt.year
    yearly_growth = df_cohort.groupby(['YEAR','BRAND_TYPE']).size().reset_index(name='NEW_PROPERTIES')

    q4_brand_color_map = {
        'RedDoorz': color_map_brand.get('RedDoorz', "#BD5354"),
        'Koolkost': color_map_brand.get('Koolkost', '#FF7F50'),
        'RedPartner': color_map_brand.get('RedPartner', '#8B0000')
    }
    brands_present = list(yearly_growth['BRAND_TYPE'].unique())
    final_q4_map = {b: q4_brand_color_map.get(b, reddoorz_palette[2]) for b in brands_present}

    st.markdown("<div class='chart-hover'>", unsafe_allow_html=True)
    fig_q4 = px.line(
        yearly_growth, x='YEAR', y='NEW_PROPERTIES', color='BRAND_TYPE',
        markers=True, color_discrete_map=final_q4_map, line_dash='BRAND_TYPE',
        labels={'NEW_PROPERTIES':'Jml Properti Baru','YEAR':'Tahun'}
    )
    fig_q4.update_traces(marker=dict(size=8))
    fig_q4.update_xaxes(type='category')
    fig_q4.update_layout(margin=dict(t=10,b=10,l=10,r=10), hovermode='x unified')
    st.plotly_chart(fig_q4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Insight Q4
    st.info("""
    **Temuan Kritis**: **RedDoorz** ($46$ unit di 2022) dan **KoolKost** ($43$ unit di 2023) adalah *driver* pertumbuhan kuantitas yang agresif. Temuan ini **bertolak belakang dengan Q1**, menunjukkan akuisisi memprioritaskan **volume di atas kualitas aset**.
    **Rekomendasi Strategi**: 1) **Moratorium Akuisisi RedPartner**: Alihkan modal dari akuisisi RedPartner ke **perbaikan aset Grade C/D** yang ada untuk peningkatan kinerja yang pasti. 2) **Ubah Metrik BD (Business Development)**: Ukur tim akuisisi TIDAK dari *jumlah* aset baru, tetapi dari **persentase properti baru yang mencapai Grade C dalam 6 bulan**.
    """)