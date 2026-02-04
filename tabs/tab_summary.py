# tabs/tab_summary.py

import streamlit as st
import re

def render_tab():
    """Render Tab 4: Rangkuman Aksi Strategis"""
    
    st.subheader("Rangkuman Aksi Strategis Portofolio")
    
    st.markdown("""
    <style>
    .summary-card {
        background-color: #f7f7f7; 
        border-left: 5px solid #EB3638; 
        padding: 15px; 
        margin-bottom: 20px;
        border-radius: 8px;
    }
    .summary-title {
        font-size: 18px;
        font-weight: 700;
        color: #8B0000;
        margin-bottom: 5px;
    }
    .kritis { color: #EB3638; font-weight: 700; }
    .aksi { color: #FF7F50; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### Rekomendasi Prioritas Berdasarkan Tujuan Bisnis Utama (Q1 - Q5)")
    
    # Data Konsolidasi
    data_summary = [
        {
            'Aspek': 'Kualitas Aset & Konsolidasi',
            'Temuan Kritis': '**95.4%** aset adalah **Grade E** (krisis volume). Ekspansi agresif RedPartner/KoolKost menambah volume aset berkinerja buruk.',
            'Aksi Rekomendasi': 'Fokus **Delisting Agresif** properti E yang terburuk. Alihkan modal ke **Perbaikan Intensif aset Grade C/D** (aset potensial ~4%). Tim BD diukur berdasarkan **kualitas (Grade C/B)**, bukan volume akuisisi mentah.',
            'Konteks': 'Q1, Q4'
        },
        {
            'Aspek': 'Pricing & Revenue Management',
            'Temuan Kritis': '**ADR Seragam** (sekitar $5.00) di semua *brand* dan kota (**Q2**), menunjukkan **kegagalan diferensiasi nilai**. KoolKost tidak memberikan insentif harga *long-stay*.',
            'Aksi Rekomendasi': 'Terapkan **diskon volume wajib (15%–20%)** untuk KoolKost. Segera uji kenaikan ADR ($+0.50) di properti Grade C/D di pasar terkuat (**Yogyakarta/Jakarta**) untuk membangun *pricing power* yang hilang.',
            'Konteks': 'Q2, Q3'
        },
        {
            'Aspek': 'Loyalitas & Pengalaman Pelanggan (QoE)',
            'Temuan Kritis': 'Korelasi loyalitas sangat lemah: Grade A hanya 2% Repeat User lebih tinggi dari Grade E. Okupansi tinggi TIDAK secara otomatis berarti kualitas pengalaman superior.',
            'Aksi Rekomendasi': 'Lakukan **Audit Kualitas Pengalaman (QoE)** pada properti Grade A. **Re-evaluasi metrik Grade** untuk memasukkan *Rating* atau *NPS* agar Grade A benar-benar mencerminkan kualitas superior yang memicu loyalitas.',
            'Konteks': 'Q5'
        }
    ]

    # Render Tabel
    html_table = """
    <table class="styled-table">
        <thead>
            <tr>
                <th style="width: 18%; background-color:#EB3638;">Aspek Kunci</th>
                <th style="width: 42%; background-color:#EB3638;">Temuan Kritis (Insight)</th>
                <th style="width: 40%; background-color:#EB3638;">Aksi Strategis Prioritas</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for item in data_summary:
        # Clean LaTeX syntax
        raw_krit = item['Temuan Kritis'].replace(r'\mathbf{', '').replace('}', '').replace(r'\sim', '~').replace(r'\mathbf', '').replace(r'\$', '$')
        raw_aksi = item['Aksi Rekomendasi'].replace(r'\mathbf{', '').replace('}', '').replace(r'\$', '$')

        # Convert Markdown to HTML
        krit_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_krit)
        aksi_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_aksi)
        
        krit_html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', krit_html)
        aksi_html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', aksi_html)

        html_table += f"""
<tr>
    <td style="font-weight: 700; color: #8B0000;">{item['Aspek']}</td>
    <td>{krit_html}</td>
    <td style="font-style: italic;">{aksi_html}</td>
</tr>
"""
    html_table += "</tbody></table>"

    st.markdown(html_table, unsafe_allow_html=True)