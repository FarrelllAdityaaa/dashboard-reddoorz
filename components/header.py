# components/header.py

import streamlit as st
from config.styles import style_metric_cards

def render_title(start_date, end_date):
    """Render title dengan periode analisis"""
    st.title("🏨 RedDoorz Portfolio Performance Dashboard")
    st.markdown(f"Periode Analisis: **{start_date}** s/d **{end_date}**")

def render_business_context():
    """Render business context expander dengan info box dan panduan"""
    with st.expander("ℹ️  KONTEKS BISNIS DAN PANDUAN ANALISIS (Klik untuk membuka)", expanded=True):
        style_metric_cards()
        
        c1, c2 = st.columns([1,1])
        with c1:
            st.markdown("""
            <div class="info-box" style="height: 100%;">
                <div class="info-title">TUJUAN BISNIS UTAMA</div>
                <div class="info-text">
                Menganalisis performa operasional dan profitabilitas portofolio RedDoorz untuk:
                <ul style="margin-top: 5px;">
                    <li><b>Identifikasi Aset Unggul (Replicate):</b> Meniru strategi properti Grade A.</li>
                    <li><b>Identifikasi Aset Lemah (Fix):</b> Memperbaiki atau delisting properti Grade E.</li>
                </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="info-box" style="height: 100%;">
                <div class="info-title">PROFIL BRAND</div>
                <div class="info-text">
                <b>1. RedDoorz (Core):</b><br>Harian, Budget, Wisatawan/Bisnis Singkat. Fasilitas standar.<br><br>
                <b>2. KoolKost (Co-Living):</b><br>Jangka Panjang (>7 hari), Kost, Mahasiswa/Pekerja. Low margin, High stability.<br><br>
                <b>3. RedPartner (Mitra):</b><br>Kemitraan lokal (Guesthouse), dikelola mitra, variatif.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-title" style="margin-top: 20px;">PANDUAN VISUALISASI & PERTANYAAN BISNIS</div>
        <table class="styled-table">
            <thead>
                <tr>
                    <th style="width: 5%;">Kode</th>
                    <th style="width: 40%;">Pertanyaan Bisnis (Analisis)</th>
                    <th style="width: 15%;">Jenis Chart</th>
                    <th>Deskripsi & Insight yang Dicari</th>
                </tr>
            </thead>
            <tbody>
                <tr title="Komposisi Performa Okupansi Properti (Grade A-E)">
                    <td><b>Q1</b></td>
                    <td>Komposisi Performa Okupansi Properti (Grade A-E)</td>
                    <td>Pie Chart</td>
                    <td>Mendiagnosis proporsi aset yang "Baik" (Grade A) vs "Buruk" (Grade E) dalam portofolio.</td>
                </tr>
                <tr title="Perbandingan Harga (ADR) per Brand">
                    <td><b>Q2</b></td>
                    <td>Perbandingan Harga (ADR) per Brand</td>
                    <td>Bar Chart</td>
                    <td>Mengukur kemampuan setiap brand menghasilkan nilai dari setiap kamar yang terjual (ADR).</td>
                </tr>
                <tr title="Peringkat kota berdasarkan revenue">
                    <td><b>Q3</b></td>
                    <td>Peringkat Kota Berdasarkan Revenue</td>
                    <td>Bar Chart</td>
                    <td>Identifikasi kota "Mesin Uang" & apakah didorong oleh volume (okupansi) atau harga (ADR).</td>
                </tr>
                <tr title="Tren Pertumbuhan Properti Baru (Tahunan)">
                    <td><b>Q4</b></td>
                    <td>Tren Pertumbuhan Properti Baru (Tahunan)</td>
                    <td>Line Chart</td>
                    <td>Memantau laju ekspansi/akuisisi properti dari tahun ke tahun untuk setiap brand.</td>
                </tr>
                <tr title="Proporsi Loyalitas (Grade A vs Grade E)">
                    <td><b>Q5</b></td>
                    <td>Proporsi Loyalitas (Grade A vs Grade E)</td>
                    <td>Bar Chart & Uji Statistik</td>
                    <td>Menguji apakah Grade A berkorelasi dengan proporsi Repeat User dibanding Grade E.</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

def render_kpi_cards(kpis):
    """
    Render KPI metric cards
    kpis: dict dari calculate_kpis()
    """
    from utils.calculations import format_revenue_display
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Format values
    formatted_revenue = format_revenue_display(kpis['total_revenue'])
    real_revenue = f"${kpis['total_revenue']:,.2f}"
    real_bookings = f"{kpis['total_bookings']:,}"
    real_nights = f"{kpis['total_nights']:,}"
    real_adr = f"${kpis['avg_adr']:,.2f}"
    real_retention = f"{kpis['retention_rate']:.2f}%"
    
    with col1:
        st.metric(
            "Total Revenue", 
            formatted_revenue, 
            help=f"💰 Nilai Lengkap: {real_revenue}\n\nTotal pendapatan dalam periode terpilih."
        )
    with col2:
        st.metric(
            "Total Transaksi", 
            f"{kpis['total_bookings']:,}",
            help=f"🧾 Nilai Lengkap: {real_bookings}\n\nJumlah Booking ID Unik yang tercatat."
        )
    with col3:
        st.metric(
            "Room Nights", 
            f"{kpis['total_nights']:,}", 
            help=f"🛏️ Nilai Lengkap: {real_nights}\n\nTotal malam kamar terjual."
        )
    with col4:
        st.metric(
            "Avg ADR", 
            f"${kpis['avg_adr']:,.2f}", 
            help=f"🏷️ Nilai Lengkap: {real_adr}\n\nAverage Daily Rate (Rata-rata harga per malam)."
        )
    with col5:
        st.metric(
            "Retention Rate", 
            f"{kpis['retention_rate']:.1f}%", 
            help=f"👥 Nilai Lengkap: {real_retention}\n\nPersentase user unik yang melakukan transaksi lebih dari sekali (Repeat User)."
        )
