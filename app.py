import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
import textwrap
from streamlit import components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="RedDoorz Performance Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Matikan warning
warnings.filterwarnings('ignore')

# --- DEFINISI PALET WARNA KUSTOM (Sesuai Diskusi) ---
color_map_brand = {
    'RedDoorz': '#EB3638',   # Merah Signature
    'RedPartner': '#8B0000', # Merah Gelap/Maroon
    'Koolkost': '#FF7F50'    # Coral/Oranye
}

# Warna Kota (Menggunakan palet kontras yang kita sepakati untuk Q3)
color_map_city = {
    'Yogyakarta': '#1f77b4', # Biru
    'Bandung': '#ff7f0e',    # Oranye
    'Jakarta': '#2ca02c',    # Hijau
    'Malang': '#d62728',     # Merah
    'Surabaya': '#9467bd'    # Ungu
}

# Warna Grade (Gradasi Emas ke Merah Gelap)
color_map_grade = {
    'A': '#FFD700', # Emas
    'B': '#FFA500', # Oranye
    'C': '#FF4500', # Oranye Merah
    'D': '#B22222', # Merah Bata
    'E': '#800000'  # Maroon Gelap
}

def style_metric_cards(
    background_color="#FFFFFF",
    border_left_color="#EB3638",
    border_color="#E6E6E6",
    box_shadow=True
):
    box_shadow_css = "box-shadow: 0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24);" if box_shadow else ""
    
    st.markdown(
        f"""
        <style>
        div[data-testid="stMetric"] {{
            background-color: {background_color};
            border: 1px solid {border_color};
            padding: 15px;
            border-radius: 10px;
            border-left: 6px solid {border_left_color};
            {box_shadow_css}
        }}
        /* Mengatur warna label (judul kecil di atas) */
        div[data-testid="stMetric"] label {{
            color: #6c757d;
            font-size: 14px;
        }}
        /* Mengatur warna value (angka besar) */
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
            color: #2D2D2D;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- 2. FUNGSI LOAD DATA & CACHING ---
@st.cache_data
def load_data():
    try:
        # Load Dataframes
        df_bookings = pd.read_csv("Online Budget Hotel Dataset.xlsx - Bookings Table.csv")
        df_property = pd.read_csv("Online Budget Hotel Dataset.xlsx - Property Table.csv")
        df_user = pd.read_csv("Online Budget Hotel Dataset.xlsx - User Table.csv")
        
        # Cleaning Sederhana
        for df in [df_bookings, df_property, df_user]:
            df.drop(columns=[col for col in df.columns if 'Unnamed' in col], inplace=True, errors='ignore')

        # Convert Date & Numeric
        df_bookings['CHECK_IN_DATE'] = pd.to_datetime(df_bookings['CHECK_IN_DATE'], errors='coerce')
        df_property['COHORT_DATE'] = pd.to_datetime(df_property['COHORT_DATE'], errors='coerce')
        
        df_bookings['REVENUE_DOLLAR'] = pd.to_numeric(df_bookings['REVENUE_DOLLAR'], errors='coerce')
        df_bookings['ROOM_NIGHTS'] = pd.to_numeric(df_bookings['ROOM_NIGHTS'], errors='coerce')
        df_property['INVENTORY'] = pd.to_numeric(df_property['INVENTORY'], errors='coerce')

        # Merge Utama
        df_merged = pd.merge(
            df_bookings,
            df_property[['PROPERTY_CODE', 'BRAND_TYPE', 'CITY', 'INVENTORY']],
            on='PROPERTY_CODE',
            how='left'
        )
        
        # Merge User
        df_merged_user = pd.merge(
            df_merged,
            df_user[['USER_ID', 'USER_TYPE', 'USER_GENDER']],
            on='USER_ID',
            how='left'
        )

        return df_merged_user, df_property
        
    except FileNotFoundError:
        return None, None

# Load Data
df_main, df_prop_raw = load_data()

if df_main is None:
    st.error("❌ File CSV tidak ditemukan. Pastikan 3 file dataset ada di folder yang sama dengan app.py")
    st.stop()

# --- 3. SIDEBAR FILTER ---
st.sidebar.image("https://i0.wp.com/join.reddoorz.com/wp-content/uploads/2022/12/rdlogo.png?fit=960%2C434&ssl=1", width=200)
# st.sidebar.markdown("<h3 style='text-align: left;'>Tim: SAFARI DATA 🐱</h3>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("## 🔍 Filter Data")


# --- A. Filter Kategori (Brand & Kota) Dulu ---
# (Lebih intuitif bagi user untuk memilih ini dulu)

all_brands = sorted(df_main['BRAND_TYPE'].dropna().unique())
selected_brands = st.sidebar.multiselect("🏷️ Pilih Brand:", all_brands, default=all_brands)

all_cities = sorted(df_main['CITY'].dropna().unique())
selected_cities = st.sidebar.multiselect("🏙️ Pilih Kota:", all_cities, default=all_cities)

st.sidebar.divider() # Pemisah visual agar rapi

# --- B. Filter Tanggal (Dipindahkan ke Tengah) ---
# Kita persingkat labelnya agar tidak kepotong
min_date = df_main['CHECK_IN_DATE'].min()
max_date = df_main['CHECK_IN_DATE'].max()

start_date, end_date = st.sidebar.date_input(
    "📅 Periode Check-In:",  # Label lebih pendek
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# --- C. Logika Hitung Grade (Di Balik Layar) ---
# (Tetap dijalankan setelah tanggal dipilih, tapi sebelum filter Grade ditampilkan)
days_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1

# Filter sementara untuk hitung inventory aktif
temp_df = df_main[
    (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) & 
    (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
]

prop_agg = temp_df.groupby('PROPERTY_CODE').agg(
    SOLD=('ROOM_NIGHTS', 'sum')
).reset_index()

# Ambil inventory dari master data sesuai filter brand/kota
active_props = df_prop_raw[
    (df_prop_raw['BRAND_TYPE'].isin(selected_brands)) &
    (df_prop_raw['CITY'].isin(selected_cities))
][['PROPERTY_CODE', 'INVENTORY']]

prop_final = pd.merge(active_props, prop_agg, on='PROPERTY_CODE', how='left').fillna(0)
prop_final['AVAILABLE'] = prop_final['INVENTORY'] * days_count

prop_final['OCC'] = 0
mask = prop_final['AVAILABLE'] > 0
prop_final.loc[mask, 'OCC'] = (prop_final.loc[mask, 'SOLD'] / prop_final.loc[mask, 'AVAILABLE']) * 100

def get_grade_logic(x):
    if x > 80: return 'A'
    elif x >= 70: return 'B'
    elif x >= 40: return 'C'
    elif x >= 20: return 'D'
    else: return 'E'

prop_final['GRADE'] = prop_final['OCC'].apply(get_grade_logic)

# Mapping balik ke dataframe utama
grade_mapping = dict(zip(prop_final['PROPERTY_CODE'], prop_final['GRADE']))
df_main['CURRENT_GRADE'] = df_main['PROPERTY_CODE'].map(grade_mapping).fillna('E')

# --- D. Filter Grade (Paling Bawah) ---
st.sidebar.markdown("---") # Garis tipis
all_grades = ['A', 'B', 'C', 'D', 'E']
selected_grades = st.sidebar.multiselect("⭐ Filter Kualitas (Grade):", all_grades, default=all_grades)

# --- E. Terapkan Semua Filter ---
filtered_df = df_main[
    (df_main['BRAND_TYPE'].isin(selected_brands)) &
    (df_main['CITY'].isin(selected_cities)) &
    (df_main['CURRENT_GRADE'].isin(selected_grades)) &
    (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) &
    (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
]

# --- 4. KPI UTAMA (HEADER) ---
st.title("🏨 Dashboard Analisis Bisnis RedDoorz")
st.markdown(f"Periode Analisis: **{start_date}** s/d **{end_date}**")

# Terapkan Styling Kartu Metric
style_metric_cards()

col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_df['REVENUE_DOLLAR'].sum()
total_bookings = filtered_df['BOOKING_ID'].nunique()
total_nights = filtered_df['ROOM_NIGHTS'].sum()
avg_adr = total_revenue / total_nights if total_nights > 0 else 0

# 1. Total Revenue (Disingkat jadi Juta/Miliar biar muat)
# Logic: Jika jutaan pakai M, jika ribuan pakai K
if total_revenue >= 1_000_000:
    formatted_revenue = f"${total_revenue/1_000_000:.2f} M"
elif total_revenue >= 1_000:
    formatted_revenue = f"${total_revenue/1_000:.2f} K"
else:
    formatted_revenue = f"${total_revenue:,.2f}"

col1.metric(
    "Total Revenue", 
    formatted_revenue, # Tampilkan angka pendek
    help=f"Total Pendapatan Asli: ${total_revenue:,.2f}" # Tooltip angka panjang
)

# 2. Total Transaksi
col2.metric(
    "Total Transaksi", 
    f"{total_bookings:,}", 
    help=f"Jumlah Booking ID Unik: {total_bookings}"
)

# 3. Total Room Nights
col3.metric(
    "Total Room Nights", 
    f"{total_nights:,}",
    help="Total malam kamar terjual"
)

# 4. ADR
col4.metric(
    "Rata-rata ADR", 
    f"${avg_adr:,.2f}",
    help="Average Daily Rate (Revenue / Room Nights)"
)

st.divider()

# --- 5. TABS ANALISIS ---
tab1, tab2, tab3 = st.tabs(["📊 1. Aset & Kualitas", "🗺️ 2. Wilayah & Revenue", "👥 3. Pelanggan & Loyalitas"])

# ==============================================================================
# TAB 1: Aset & Kualitas (Q1 & Q4)
# ==============================================================================
with tab1:
    col_q1, col_q4 = st.columns(2)
    
    # --- Q1: Distribusi Grade (Menggunakan Occupancy Periode Ini) ---
    with col_q1:
        st.subheader("Q1: Distribusi Kualitas Properti (Grade)")
        
        # Hitung Okupansi Agregat per Properti
        prop_agg = filtered_df.groupby('PROPERTY_CODE').agg(
            SOLD=('ROOM_NIGHTS', 'sum'),
            INVENTORY=('INVENTORY', 'max')
        ).reset_index()
        
        days_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1
        prop_agg['AVAILABLE'] = prop_agg['INVENTORY'] * days_count
        prop_agg['OCC'] = (prop_agg['SOLD'] / prop_agg['AVAILABLE']) * 100
        
        def get_grade(x):
            if x > 80: return 'A'
            elif x >= 70: return 'B'
            elif x >= 40: return 'C'
            elif x >= 20: return 'D'
            else: return 'E'
            
        prop_agg['GRADE'] = prop_agg['OCC'].apply(get_grade)
        grade_dist = prop_agg['GRADE'].value_counts().reset_index()
        grade_dist.columns = ['GRADE', 'COUNT']
        
        fig_q1 = px.pie(
            grade_dist, names='GRADE', values='COUNT',
            color='GRADE', color_discrete_map=color_map_grade,
            hole=0.4,
            category_orders={'GRADE': ['A', 'B', 'C', 'D', 'E']}
        )
        fig_q1.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig_q1, use_container_width=True)
        
        st.info("Insight Q1: Mayoritas portofolio berada di Grade E (<20% Okupansi).")

    # --- Q4: Tren Pertumbuhan (Line Chart) ---
    with col_q4:
        st.subheader("Q4: Tren Akuisisi Properti Baru (Tahunan)")
        
        # Gunakan data properti mentah untuk melihat sejarah kohort
        df_cohort = df_prop_raw[df_prop_raw['BRAND_TYPE'].isin(selected_brands)].copy()
        df_cohort['YEAR'] = df_cohort['COHORT_DATE'].dt.year
        
        yearly_growth = df_cohort.groupby(['YEAR', 'BRAND_TYPE']).size().reset_index(name='NEW_PROPERTIES')
        
        fig_q4 = px.line(
            yearly_growth, x='YEAR', y='NEW_PROPERTIES', color='BRAND_TYPE',
            markers=True, color_discrete_map=color_map_brand,
            labels={'NEW_PROPERTIES': 'Jml Properti Baru', 'YEAR': 'Tahun'}
        )
        fig_q4.update_xaxes(type='category') # Agar tahun tidak ada koma
        st.plotly_chart(fig_q4, use_container_width=True)
        
        st.info("Insight Q4: RedDoorz memuncak di 2022, Koolkost agresif di 2023.")

# ==============================================================================
# TAB 2: Wilayah & Revenue (Q3)
# ==============================================================================
with tab2:
    st.subheader("Q3: Peringkat Kota Berdasarkan Revenue & Driver Utamanya")
    
    # Agregasi Data Kota
    city_agg = filtered_df.groupby('CITY').agg(
        TOTAL_REVENUE=('REVENUE_DOLLAR', 'sum'),
        TOTAL_SOLD=('ROOM_NIGHTS', 'sum')
    ).reset_index()
    
    # Hitung Inventory Kota (Unik)
    city_inv = filtered_df[['PROPERTY_CODE', 'CITY', 'INVENTORY']].drop_duplicates() \
               .groupby('CITY')['INVENTORY'].sum().reset_index()
    
    df_city = pd.merge(city_agg, city_inv, on='CITY')
    
    # Hitung Metrik
    df_city['ADR'] = df_city['TOTAL_REVENUE'] / df_city['TOTAL_SOLD']
    df_city['OCCUPANCY'] = (df_city['TOTAL_SOLD'] / (df_city['INVENTORY'] * days_count)) * 100
    
    df_city_sorted = df_city.sort_values('TOTAL_REVENUE', ascending=False)

    fig_q3 = px.bar(
        df_city_sorted,
        x='CITY', y='TOTAL_REVENUE', color='CITY',
        color_discrete_map=color_map_city,
        text_auto='.2s',
        hover_data={
            'TOTAL_REVENUE':':.2f', 'ADR':':.2f', 
            'OCCUPANCY':':.2f', 'INVENTORY':True, 'CITY':False
        },
        labels={'TOTAL_REVENUE': 'Total Revenue ($)', 'CITY': 'Kota'}
    )
    # Style agar mirip gambar referensi Anda
    fig_q3.update_traces(textposition='inside')
    fig_q3.update_layout(
        xaxis={'categoryorder':'total descending'},
        hoverlabel=dict(bgcolor="black", font_color="white", bordercolor="black")
    )
    
    st.plotly_chart(fig_q3, use_container_width=True)
    
    st.info("""
    **Insight Q3:** Yogyakarta memimpin revenue ($427k) murni karena volume inventaris terbesar. 
    Secara performa (ADR ~$5.00 dan Okupansi ~0.75%), semua kota sangat identik/terstandarisasi.
    """)

# ==============================================================================
# TAB 3: Pelanggan (Q2 & Q5)
# ==============================================================================
with tab3:
    col_q2, col_q5 = st.columns(2)
    
    # --- Q2: ADR per Brand ---
    with col_q2:
        st.subheader("Q2: Perbandingan Harga (ADR) per Brand")
        
        brand_perf = filtered_df.groupby('BRAND_TYPE').agg(
            REV=('REVENUE_DOLLAR', 'sum'),
            RN=('ROOM_NIGHTS', 'sum')
        ).reset_index()
        brand_perf['ADR'] = brand_perf['REV'] / brand_perf['RN']
        
        fig_q2 = px.bar(
            brand_perf, x='BRAND_TYPE', y='ADR', color='BRAND_TYPE',
            color_discrete_map=color_map_brand,
            text_auto='.2f',
            labels={'ADR': 'Rata-rata Harga ($)'}
        )
        fig_q2.update_layout(yaxis_range=[0, 6]) # Agar skala terlihat wajar
        st.plotly_chart(fig_q2, use_container_width=True)
        
        st.info("Insight Q2: Strategi harga sangat seragam ($4.98 - $5.01) antar brand.")
        
    # --- Q5: Loyalitas Pelanggan ---
    with col_q5:
        st.subheader("Q5: Proporsi Loyalitas (Global)")
        
        user_type_counts = filtered_df['USER_TYPE'].value_counts().reset_index()
        user_type_counts.columns = ['USER_TYPE', 'COUNT']
        
        fig_q5 = px.pie(
            user_type_counts, names='USER_TYPE', values='COUNT',
            color='USER_TYPE',
            color_discrete_map={'New User': '#1f77b4', 'Repeat User': '#ff7f0e'}, # Biru vs Oranye (Kontras)
            hole=0.5
        )
        st.plotly_chart(fig_q5, use_container_width=True)
        
        st.info("""
        **Insight Q5:** Secara global, rasio New vs Repeat hampir seimbang (50:50).
        Analisis lebih dalam menunjukkan Properti Grade E justru memiliki retensi lebih tinggi dari Grade A.
        """)

# --- 6. FOOTER TIM VISUALISASI ---

footer_css = """
<style>
.footer-container {
    background: transparent;
    padding: 18px 12px;
    border-radius: 10px;
    text-align: center;
    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #333333;
    
    /* --- PERUBAHAN DI SINI --- */
    margin-top: 170px;  /* Memberi jarak jauh ke bawah dari konten sebelumnya */
    border-top: 3px solid #EB3638; /* Garis pemisah merah tipis di atas footer */
    padding-top: 30px; /* Jarak antara garis dan teks footer */
}
.footer-container .sponsor {
    color: #666666;
    font-size: 14px;
    margin-bottom: 6px;
}
.footer-container h2 {
    color: #EB3638 !important;   /* Merah signature */
    font-weight: 800;
    letter-spacing: 1px;
    margin: 0;
    font-size: 20px;
}
.footer-container .team {
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    margin-top: 12px;
    color: #2D2D2D;
    font-weight: 600;
    font-size: 15px;
}
.footer-container .copyright {
    color: #999999;
    font-size: 12px;
    margin-top: 18px;
}
@media (max-width: 600px) {
    .footer-container .team { font-size: 14px; gap: 10px; }
    .footer-container h2 { font-size: 18px; }
}
</style>
"""

footer_html = """
<div class="footer-container">
  <div class="sponsor">Dashboard ini dipersembahkan oleh:</div>
  <h2>📊 SAFARI DATA 🐱</h2>
  <div class="team">
    <span>👩‍💻 Nabila Putri Asy Syifa</span>
    <span style="color: #EB3638;">|</span>
    <span>👨‍💻 Farrel Paksi Aditya</span>
    <span style="color: #EB3638;">|</span>
    <span>👩‍💻 Nur Salamah Azzahrah</span>
  </div>
  <div class="copyright">© 2024 Proyek Akhir Visualisasi Data | RedDoorz Analysis</div>
</div>
"""

# Gabungkan CSS dan HTML
html_full = footer_css + textwrap.dedent(footer_html)
st.markdown(html_full, unsafe_allow_html=True)