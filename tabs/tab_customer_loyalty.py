# tabs/tab_customer_loyalty.py

import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import color_map_brand, reddoorz_palette

def render_tab(filtered_df):
    """Render Tab 3: Pelanggan & Loyalitas"""
    
    st.subheader("Q2: Perbandingan Harga (ADR) per Brand")

    brand_perf = filtered_df.groupby('BRAND_TYPE').agg(
        REV=('REVENUE_DOLLAR','sum'), 
        RN=('ROOM_NIGHTS','sum')
    ).reset_index()
    brand_perf['ADR'] = brand_perf.apply(lambda r: (r['REV']/r['RN']) if r['RN'] and r['RN']>0 else 0, axis=1)

    # Color mapping
    brands_present = brand_perf['BRAND_TYPE'].tolist()
    final_brand_map = {}
    for i, b in enumerate(brands_present):
        final_brand_map[b] = color_map_brand.get(b, reddoorz_palette[i % len(reddoorz_palette)])

    brand_perf['TEXT'] = brand_perf['ADR'].apply(lambda x: f"{x:.2f}")
    
    fig_q2 = px.bar(
        brand_perf, x='BRAND_TYPE', y='ADR', color='BRAND_TYPE',
        color_discrete_map=final_brand_map, text='TEXT',
        labels={'ADR':'Rata-rata Harga ($)','BRAND_TYPE':'Brand'},
        hover_data={'REV':':,.0f','RN':':,.0f','ADR':':.2f','BRAND_TYPE':False}
    )
    fig_q2.update_traces(textposition='outside', marker_line_width=1, marker_line_color='rgba(0,0,0,0.08)')
    fig_q2.update_layout(
        yaxis_range=[0, max(brand_perf['ADR'].max()*1.15, 6)], 
        uniformtext_minsize=10, 
        uniformtext_mode='hide', 
        showlegend=True, 
        legend_title_text='Brand', 
        margin=dict(t=30,b=20,l=40,r=20)
    )
    fig_q2.update_yaxes(tickformat='.2f')
    st.plotly_chart(fig_q2, use_container_width=True)

    # Insight Q2
    st.info("""
    **Temuan Kritis**: ADR sangat seragam (sekitar **\$5.00**) di semua brand (**RedDoorz: \$5.00, KoolKost: \$4.98, RedPartner: \$5.00**). Keseragaman ini menunjukkan **kegagalan diferensiasi nilai produk**. **KoolKost** gagal memberikan insentif harga (*ADR long-stay* seharusnya jauh lebih rendah).
    **Rekomendasi Strategi**: 1) Terapkan **diskon volume wajib** (**15% - 20%** lebih rendah) pada KoolKost untuk durasi inap panjang. 2) **Uji kenaikan harga agresif** di properti **Grade A** (Okupansi > 80%) menuju ADR **\$6.00** untuk membuktikan *pricing power* aset unggul.
    """)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Q5: Loyalitas
    st.subheader("Q5: Proporsi Loyalitas (Grade A vs Grade E)")
    subset_loyalty = filtered_df[filtered_df['CURRENT_GRADE'].isin(['A','E'])].copy()

    if not subset_loyalty.empty:
        loyalty_analysis = (
            subset_loyalty.groupby('CURRENT_GRADE')['USER_TYPE']
            .apply(lambda x: (x == 'Repeat User').mean())
            .reset_index(name='REPEAT_RATIO')
        )
        ref_grades = pd.DataFrame({'CURRENT_GRADE':['A','E']})
        loyalty_final = ref_grades.merge(loyalty_analysis, on='CURRENT_GRADE', how='left').fillna(0)

        # Custom Color Map for A and E
        reddoorz_grade_map_ae = {
            'A': '#EB3638',  # Merah (primary)
            'E': '#FF7F50'   # Oranye Koral (Koolkost / accent)
        }
        
        fig_q5 = px.bar(
            loyalty_final, x='CURRENT_GRADE', y='REPEAT_RATIO',
            color='CURRENT_GRADE', color_discrete_map=reddoorz_grade_map_ae,
            text_auto='.1%', 
            labels={'CURRENT_GRADE':'Grade Properti','REPEAT_RATIO':'Proporsi Repeat User'}
        )
        fig_q5.update_traces(textposition='outside')
        fig_q5.update_layout(
            yaxis_title="Proporsi Repeat User", 
            yaxis=dict(tickformat=".0%"), 
            showlegend=True,
            legend_title_text="Grade",
            margin=dict(t=20,b=20,l=20,r=20), 
            height=300, 
            yaxis_range=[0,1]
        )
        st.plotly_chart(fig_q5, use_container_width=True)

        st.markdown("**Tabel proporsi Repeat User per Grade (A vs E)**")
        st.dataframe(loyalty_final.style.format({'REPEAT_RATIO':'{:.1%}'}))

        # Insight Q5
        st.info("""
        **Temuan Kritis**: Proporsi **Repeat User** di Grade A (49.2%) hanya sedikit lebih tinggi (2%) dari Grade E (47.2%). Perbedaan ini **terlalu kecil** untuk memvalidasi ROI kualitas aset secara kuat.
        **Rekomendasi Strategi**: 1) **Audit Kualitas Pengalaman (QoE)** properti Grade A (Okupansi tinggi) untuk mengidentifikasi dan mereplikasi *unique selling points* yang benar-benar menciptakan loyalitas. 2) **Re-evaluasi metrik Grade** untuk memasukkan *Rating* atau *NPS* agar Grade A benar-benar mencerminkan kualitas superior.
        """)
    else:
        st.warning("Data tidak cukup untuk membandingkan Grade A dan Grade E pada filter yang dipilih.")