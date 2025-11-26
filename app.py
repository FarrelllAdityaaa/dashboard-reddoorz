# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import warnings
# import textwrap
# from streamlit import components

# # --- 1. KONFIGURASI HALAMAN ---
# st.set_page_config(
#     page_title="RedDoorz Performance Dashboard",
#     page_icon="🏨",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Matikan warning
# warnings.filterwarnings('ignore')

# # --- DEFINISI PALET WARNA KUSTOM (Sesuai Diskusi) ---
# color_map_brand = {
#     'RedDoorz': '#EB3638',   # Merah Signature
#     'RedPartner': '#8B0000', # Merah Gelap/Maroon
#     'Koolkost': '#FF7F50'    # Coral/Oranye
# }

# # Warna Kota (Menggunakan palet kontras yang kita sepakati untuk Q3)
# color_map_city = {
#     'Yogyakarta': '#1f77b4', # Biru
#     'Bandung': '#ff7f0e',    # Oranye
#     'Jakarta': '#2ca02c',    # Hijau
#     'Malang': '#d62728',     # Merah
#     'Surabaya': '#9467bd'    # Ungu
# }

# # Warna Grade (Gradasi Emas ke Merah Gelap)
# color_map_grade = {
#     'A': '#FFD700', # Emas
#     'B': '#FFA500', # Oranye
#     'C': '#FF4500', # Oranye Merah
#     'D': '#B22222', # Merah Bata
#     'E': '#800000'  # Maroon Gelap
# }

# def style_metric_cards(
#     background_color="#FFFFFF",
#     border_left_color="#EB3638",
#     border_color="#E6E6E6",
#     box_shadow=True
# ):
#     box_shadow_css = "box-shadow: 0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24);" if box_shadow else ""
    
#     st.markdown(
#         f"""
#         <style>
#         div[data-testid="stMetric"] {{
#             background-color: {background_color};
#             border: 1px solid {border_color};
#             padding: 15px;
#             border-radius: 10px;
#             border-left: 6px solid {border_left_color};
#             {box_shadow_css}
#         }}
#         /* Mengatur warna label (judul kecil di atas) */
#         div[data-testid="stMetric"] label {{
#             color: #6c757d;
#             font-size: 14px;
#         }}
#         /* Mengatur warna value (angka besar) */
#         div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
#             color: #2D2D2D;
#             font-weight: bold;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # --- 2. FUNGSI LOAD DATA & CACHING ---
# @st.cache_data
# def load_data():
#     try:
#         # Load Dataframes
#         df_bookings = pd.read_csv("Online Budget Hotel Dataset.xlsx - Bookings Table.csv")
#         df_property = pd.read_csv("Online Budget Hotel Dataset.xlsx - Property Table.csv")
#         df_user = pd.read_csv("Online Budget Hotel Dataset.xlsx - User Table.csv")
        
#         # Cleaning Sederhana
#         for df in [df_bookings, df_property, df_user]:
#             df.drop(columns=[col for col in df.columns if 'Unnamed' in col], inplace=True, errors='ignore')

#         # Convert Date & Numeric
#         df_bookings['CHECK_IN_DATE'] = pd.to_datetime(df_bookings['CHECK_IN_DATE'], errors='coerce')
#         df_property['COHORT_DATE'] = pd.to_datetime(df_property['COHORT_DATE'], errors='coerce')
        
#         df_bookings['REVENUE_DOLLAR'] = pd.to_numeric(df_bookings['REVENUE_DOLLAR'], errors='coerce')
#         df_bookings['ROOM_NIGHTS'] = pd.to_numeric(df_bookings['ROOM_NIGHTS'], errors='coerce')
#         df_property['INVENTORY'] = pd.to_numeric(df_property['INVENTORY'], errors='coerce')

#         # Merge Utama
#         df_merged = pd.merge(
#             df_bookings,
#             df_property[['PROPERTY_CODE', 'BRAND_TYPE', 'CITY', 'INVENTORY']],
#             on='PROPERTY_CODE',
#             how='left'
#         )
        
#         # Merge User
#         df_merged_user = pd.merge(
#             df_merged,
#             df_user[['USER_ID', 'USER_TYPE', 'USER_GENDER']],
#             on='USER_ID',
#             how='left'
#         )

#         return df_merged_user, df_property
        
#     except FileNotFoundError:
#         return None, None

# # Load Data
# df_main, df_prop_raw = load_data()

# if df_main is None:
#     st.error("❌ File CSV tidak ditemukan. Pastikan 3 file dataset ada di folder yang sama dengan app.py")
#     st.stop()

# # --- 3. SIDEBAR FILTER ---
# st.sidebar.image("https://i0.wp.com/join.reddoorz.com/wp-content/uploads/2022/12/rdlogo.png?fit=960%2C434&ssl=1", width=200)
# # st.sidebar.markdown("<h3 style='text-align: left;'>Tim: SAFARI DATA 🐱</h3>", unsafe_allow_html=True)
# st.sidebar.divider()
# st.sidebar.markdown("## 🔍 Filter Data")


# # --- A. Filter Kategori (Brand & Kota) Dulu ---
# # (Lebih intuitif bagi user untuk memilih ini dulu)

# all_brands = sorted(df_main['BRAND_TYPE'].dropna().unique())
# selected_brands = st.sidebar.multiselect("🏷️ Pilih Brand:", all_brands, default=all_brands)

# all_cities = sorted(df_main['CITY'].dropna().unique())
# selected_cities = st.sidebar.multiselect("🏙️ Pilih Kota:", all_cities, default=all_cities)

# st.sidebar.divider() # Pemisah visual agar rapi

# # --- B. Filter Tanggal (Dipindahkan ke Tengah) ---
# # Kita persingkat labelnya agar tidak kepotong
# min_date = df_main['CHECK_IN_DATE'].min()
# max_date = df_main['CHECK_IN_DATE'].max()

# start_date, end_date = st.sidebar.date_input(
#     "📅 Periode Check-In:",  # Label lebih pendek
#     [min_date, max_date],
#     min_value=min_date,
#     max_value=max_date
# )

# # --- C. Logika Hitung Grade (Di Balik Layar) ---
# # (Tetap dijalankan setelah tanggal dipilih, tapi sebelum filter Grade ditampilkan)
# days_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1

# # Filter sementara untuk hitung inventory aktif
# temp_df = df_main[
#     (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) & 
#     (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
# ]

# prop_agg = temp_df.groupby('PROPERTY_CODE').agg(
#     SOLD=('ROOM_NIGHTS', 'sum')
# ).reset_index()

# # Ambil inventory dari master data sesuai filter brand/kota
# active_props = df_prop_raw[
#     (df_prop_raw['BRAND_TYPE'].isin(selected_brands)) &
#     (df_prop_raw['CITY'].isin(selected_cities))
# ][['PROPERTY_CODE', 'INVENTORY']]

# prop_final = pd.merge(active_props, prop_agg, on='PROPERTY_CODE', how='left').fillna(0)
# prop_final['AVAILABLE'] = prop_final['INVENTORY'] * days_count

# prop_final['OCC'] = 0
# mask = prop_final['AVAILABLE'] > 0
# prop_final.loc[mask, 'OCC'] = (prop_final.loc[mask, 'SOLD'] / prop_final.loc[mask, 'AVAILABLE']) * 100

# def get_grade_logic(x):
#     if x > 80: return 'A'
#     elif x >= 70: return 'B'
#     elif x >= 40: return 'C'
#     elif x >= 20: return 'D'
#     else: return 'E'

# prop_final['GRADE'] = prop_final['OCC'].apply(get_grade_logic)

# # Mapping balik ke dataframe utama
# grade_mapping = dict(zip(prop_final['PROPERTY_CODE'], prop_final['GRADE']))
# df_main['CURRENT_GRADE'] = df_main['PROPERTY_CODE'].map(grade_mapping).fillna('E')

# # --- D. Filter Grade (Paling Bawah) ---
# st.sidebar.markdown("---") # Garis tipis
# all_grades = ['A', 'B', 'C', 'D', 'E']
# selected_grades = st.sidebar.multiselect("⭐ Filter Kualitas (Grade):", all_grades, default=all_grades)

# # --- E. Terapkan Semua Filter ---
# filtered_df = df_main[
#     (df_main['BRAND_TYPE'].isin(selected_brands)) &
#     (df_main['CITY'].isin(selected_cities)) &
#     (df_main['CURRENT_GRADE'].isin(selected_grades)) &
#     (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) &
#     (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
# ]

# # --- 4. KPI UTAMA (HEADER) ---
# st.title("🏨 Dashboard Analisis Bisnis RedDoorz")
# st.markdown(f"Periode Analisis: **{start_date}** s/d **{end_date}**")

# # Terapkan Styling Kartu Metric
# style_metric_cards()

# col1, col2, col3, col4 = st.columns(4)
# total_revenue = filtered_df['REVENUE_DOLLAR'].sum()
# total_bookings = filtered_df['BOOKING_ID'].nunique()
# total_nights = filtered_df['ROOM_NIGHTS'].sum()
# avg_adr = total_revenue / total_nights if total_nights > 0 else 0

# # 1. Total Revenue (Disingkat jadi Juta/Miliar biar muat)
# # Logic: Jika jutaan pakai M, jika ribuan pakai K
# if total_revenue >= 1_000_000:
#     formatted_revenue = f"${total_revenue/1_000_000:.2f} M"
# elif total_revenue >= 1_000:
#     formatted_revenue = f"${total_revenue/1_000:.2f} K"
# else:
#     formatted_revenue = f"${total_revenue:,.2f}"

# col1.metric(
#     "Total Revenue", 
#     formatted_revenue, # Tampilkan angka pendek
#     help=f"Total Pendapatan Asli: ${total_revenue:,.2f}" # Tooltip angka panjang
# )

# # 2. Total Transaksi
# col2.metric(
#     "Total Transaksi", 
#     f"{total_bookings:,}", 
#     help=f"Jumlah Booking ID Unik: {total_bookings}"
# )

# # 3. Total Room Nights
# col3.metric(
#     "Total Room Nights", 
#     f"{total_nights:,}",
#     help="Total malam kamar terjual"
# )

# # 4. ADR
# col4.metric(
#     "Rata-rata ADR", 
#     f"${avg_adr:,.2f}",
#     help="Average Daily Rate (Revenue / Room Nights)"
# )

# st.divider()

# # --- 5. TABS ANALISIS ---
# tab1, tab2, tab3 = st.tabs(["📊 1. Aset & Kualitas", "🗺️ 2. Wilayah & Revenue", "👥 3. Pelanggan & Loyalitas"])

# # ==============================================================================
# # TAB 1: Aset & Kualitas (Q1 & Q4)
# # ==============================================================================
# with tab1:
#     col_q1, col_q4 = st.columns(2)
    
#     # --- Q1: Distribusi Grade (Menggunakan Occupancy Periode Ini) ---
#     with col_q1:
#         st.subheader("Q1: Distribusi Kualitas Properti (Grade)")
        
#         # Hitung Okupansi Agregat per Properti
#         prop_agg = filtered_df.groupby('PROPERTY_CODE').agg(
#             SOLD=('ROOM_NIGHTS', 'sum'),
#             INVENTORY=('INVENTORY', 'max')
#         ).reset_index()
        
#         days_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1
#         prop_agg['AVAILABLE'] = prop_agg['INVENTORY'] * days_count
#         prop_agg['OCC'] = (prop_agg['SOLD'] / prop_agg['AVAILABLE']) * 100
        
#         def get_grade(x):
#             if x > 80: return 'A'
#             elif x >= 70: return 'B'
#             elif x >= 40: return 'C'
#             elif x >= 20: return 'D'
#             else: return 'E'
            
#         prop_agg['GRADE'] = prop_agg['OCC'].apply(get_grade)
#         grade_dist = prop_agg['GRADE'].value_counts().reset_index()
#         grade_dist.columns = ['GRADE', 'COUNT']
        
#         fig_q1 = px.pie(
#             grade_dist, names='GRADE', values='COUNT',
#             color='GRADE', color_discrete_map=color_map_grade,
#             hole=0.4,
#             category_orders={'GRADE': ['A', 'B', 'C', 'D', 'E']}
#         )
#         fig_q1.update_traces(textposition='outside', textinfo='percent+label')
#         st.plotly_chart(fig_q1, use_container_width=True)
        
#         st.info("**Insight Q1**: Mayoritas portofolio berada di Grade E (<20% Okupansi).")

#     # --- Q4: Tren Pertumbuhan (Line Chart) ---
#     with col_q4:
#         st.subheader("Q4: Tren Akuisisi Properti Baru (Tahunan)")
        
#         # Gunakan data properti mentah untuk melihat sejarah kohort
#         df_cohort = df_prop_raw[df_prop_raw['BRAND_TYPE'].isin(selected_brands)].copy()
#         df_cohort['YEAR'] = df_cohort['COHORT_DATE'].dt.year
        
#         yearly_growth = df_cohort.groupby(['YEAR', 'BRAND_TYPE']).size().reset_index(name='NEW_PROPERTIES')
        
#         fig_q4 = px.line(
#             yearly_growth, x='YEAR', y='NEW_PROPERTIES', color='BRAND_TYPE',
#             markers=True, color_discrete_map=color_map_brand,
#             labels={'NEW_PROPERTIES': 'Jml Properti Baru', 'YEAR': 'Tahun'}
#         )
#         fig_q4.update_xaxes(type='category') # Agar tahun tidak ada koma
#         st.plotly_chart(fig_q4, use_container_width=True)
        
#         st.info("**Insight Q4**: RedDoorz memuncak di 2022, Koolkost agresif di 2023.")

# # ==============================================================================
# # TAB 2: Wilayah & Revenue (Q3)
# # ==============================================================================
# with tab2:
#     st.subheader("Q3: Peringkat Kota Berdasarkan Revenue & Driver Utamanya")
    
#     # Agregasi Data Kota
#     city_agg = filtered_df.groupby('CITY').agg(
#         TOTAL_REVENUE=('REVENUE_DOLLAR', 'sum'),
#         TOTAL_SOLD=('ROOM_NIGHTS', 'sum')
#     ).reset_index()
    
#     # Hitung Inventory Kota (Unik)
#     city_inv = filtered_df[['PROPERTY_CODE', 'CITY', 'INVENTORY']].drop_duplicates() \
#                .groupby('CITY')['INVENTORY'].sum().reset_index()
    
#     df_city = pd.merge(city_agg, city_inv, on='CITY')
    
#     # Hitung Metrik
#     df_city['ADR'] = df_city['TOTAL_REVENUE'] / df_city['TOTAL_SOLD']
#     df_city['OCCUPANCY'] = (df_city['TOTAL_SOLD'] / (df_city['INVENTORY'] * days_count)) * 100
    
#     df_city_sorted = df_city.sort_values('TOTAL_REVENUE', ascending=False)

#     fig_q3 = px.bar(
#         df_city_sorted,
#         x='CITY', y='TOTAL_REVENUE', color='CITY',
#         color_discrete_map=color_map_city,
#         text_auto='.2s',
#         hover_data={
#             'TOTAL_REVENUE':':.2f', 'ADR':':.2f', 
#             'OCCUPANCY':':.2f', 'INVENTORY':True, 'CITY':False
#         },
#         labels={'TOTAL_REVENUE': 'Total Revenue ($)', 'CITY': 'Kota'}
#     )
#     # Style agar mirip gambar referensi Anda
#     fig_q3.update_traces(textposition='inside')
#     fig_q3.update_layout(
#         xaxis={'categoryorder':'total descending'},
#         hoverlabel=dict(bgcolor="black", font_color="white", bordercolor="black")
#     )
    
#     st.plotly_chart(fig_q3, use_container_width=True)
    
#     st.info("""
#     **Insight Q3:** Yogyakarta memimpin revenue (\$427k) murni karena volume inventaris terbesar. 
#     Secara performa (ADR ~\$5.00 dan Okupansi ~0.75%), semua kota sangat identik/terstandarisasi.
#     """)

# # ==============================================================================
# # TAB 3: Pelanggan (Q2 & Q5)
# # ==============================================================================
# with tab3:
#     col_q2, col_q5 = st.columns(2)
    
#     # --- Q2: ADR per Brand ---
#     with col_q2:
#         st.subheader("Q2: Perbandingan Harga (ADR) per Brand")
        
#         brand_perf = filtered_df.groupby('BRAND_TYPE').agg(
#             REV=('REVENUE_DOLLAR', 'sum'),
#             RN=('ROOM_NIGHTS', 'sum')
#         ).reset_index()
#         brand_perf['ADR'] = brand_perf['REV'] / brand_perf['RN']
        
#         fig_q2 = px.bar(
#             brand_perf, x='BRAND_TYPE', y='ADR', color='BRAND_TYPE',
#             color_discrete_map=color_map_brand,
#             text_auto='.2f',
#             labels={'ADR': 'Rata-rata Harga ($)'}
#         )
#         fig_q2.update_layout(yaxis_range=[0, 6]) # Agar skala terlihat wajar
#         st.plotly_chart(fig_q2, use_container_width=True)
        
#         st.info("**Insight Q2**: Strategi harga sangat seragam (\$4.98 - \$5.01) antar brand.")
        
#     # --- Q5: Loyalitas Pelanggan ---
#     with col_q5:
#         st.subheader("Q5: Proporsi Loyalitas (Global)")
        
#         user_type_counts = filtered_df['USER_TYPE'].value_counts().reset_index()
#         user_type_counts.columns = ['USER_TYPE', 'COUNT']
        
#         fig_q5 = px.pie(
#             user_type_counts, names='USER_TYPE', values='COUNT',
#             color='USER_TYPE',
#             color_discrete_map={'New User': '#1f77b4', 'Repeat User': '#ff7f0e'}, # Biru vs Oranye (Kontras)
#             hole=0.5
#         )
#         st.plotly_chart(fig_q5, use_container_width=True)
        
#         st.info("""
#         **Insight Q5:** Secara global, rasio New vs Repeat hampir seimbang (50:50).
#         Analisis lebih dalam menunjukkan Properti Grade E justru memiliki retensi lebih tinggi dari Grade A.
#         """)

# # --- 6. FOOTER TIM VISUALISASI ---
# footer_css = """
# <style>
# .footer-container {
#     background: transparent;
#     padding: 18px 12px;
#     border-radius: 10px;
#     text-align: center;
#     font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
#     color: #333333;
#     margin-top: 170px;  /* Memberi jarak jauh ke bawah dari konten sebelumnya */
#     border-top: 3px solid #EB3638; /* Garis pemisah merah tipis di atas footer */
#     padding-top: 30px; /* Jarak antara garis dan teks footer */
# }
# .footer-container .sponsor {
#     color: #666666;
#     font-size: 14px;
#     margin-bottom: 6px;
# }
# .footer-container h2 {
#     color: #EB3638 !important;   /* Merah signature */
#     font-weight: 800;
#     letter-spacing: 1px;
#     margin: 0;
#     font-size: 20px;
# }
# .footer-container .team {
#     display: flex;
#     justify-content: center;
#     gap: 18px;
#     flex-wrap: wrap;
#     margin-top: 12px;
#     color: #2D2D2D;
#     font-weight: 600;
#     font-size: 15px;
# }
# .footer-container .copyright {
#     color: #999999;
#     font-size: 12px;
#     margin-top: 18px;
# }

# .team-badge {
#     padding: 6px 14px;
#     border-radius: 16px;
#     color: white;
#     font-weight: 600;
#     font-size: 14px;
#     display: inline-block;
# }

# @media (max-width: 600px) {
#     .footer-container .team { font-size: 14px; gap: 10px; }
#     .footer-container h2 { font-size: 18px; }
# }
# </style>
# """

# footer_html = """
# <div class="footer-container">
#   <div class="sponsor">Dashboard ini dipersembahkan oleh:</div>
#   <h2>📊 SAFARI DATA 🐱</h2>

#   <div class="team">
#     <span class="team-badge" style="background:#FF66CC;">👩🏻‍💻 Nabila Putri Asy Syifa</span>
#     <span class="team-badge" style="background:#FFB700;">🧑🏻‍💻 Farrel Paksi Aditya</span>
#     <span class="team-badge" style="background:#2A9DF4;">👩🏻‍💻 Nur Salamah Azzahrah</span>
#   </div>

#   <div class="copyright">© 2024 Proyek Akhir Visualisasi Data | RedDoorz Analysis</div>
# </div>
# """

# # Gabungkan CSS dan HTML
# html_full = footer_css + textwrap.dedent(footer_html)
# st.markdown(html_full, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
import textwrap
import re
from streamlit import components

# NOTE: Removed global scipy import/message per user request.
# If scipy is present in the environment, the chi-square test will be attempted
# inside the Q5 block, but if not present it will fail silently (no message).

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="RedDoorz Performance Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Matikan warning
warnings.filterwarnings('ignore')

# -------------------------
# PERSISTENT HIGHLIGHT CSS
# (unchanged)
# -------------------------
persistent_highlight_css = """
<style>
/* Judul utama: beri bayangan / floating look yang selalu aktif */
.stApp .block-container h1, .stApp .block-container h1 + div {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 8px;
    box-shadow: 0 18px 48px rgba(235,54,56,0.08);
    transform: translateY(0px);
    transition: box-shadow 0.22s ease, transform 0.22s ease;
    background: transparent;
}

/* Fallback jika judul dibungkus oleh span */
.stApp .block-container h1 span {
    display: inline;
}

/* Sidebar logo: target beberapa kemungkinan selector Streamlit */
section[data-testid="stSidebar"] img,
aside img,
div[role="complementary"] img,
div.css-1offfwp img {
    display: block !important;
    margin: 10px auto !important;
    max-width: 85% !important;
    height: auto !important;
    border-radius: 8px;
    box-shadow: 0 20px 56px rgba(235,54,56,0.12);
    transform: translateY(0px);
    transition: box-shadow 0.22s ease, transform 0.22s ease;
}

/* small visual tweak for mobile / narrow sidebar */
@media (max-width: 720px) {
    section[data-testid="stSidebar"] img,
    aside img {
        max-width: 68% !important;
        box-shadow: 0 10px 30px rgba(235,54,56,0.10);
    }
}
</style>
"""

# --- DEFINISI PALET WARNA KUSTOM (REDDOORZ THEME) ---
# Core brand colors (RedDoorz theme) -- UPDATED to match user request:
# - Koolkost: Oranye Koral Terang (Bright Coral Orange)
# - RedDoorz: Merah Tua (Dark Red)
# - RedPartner: Merah Muda (Light Pink/Coral)
color_map_brand = {
    'RedDoorz': '#8B0000',    # Merah Tua
    'RedPartner': '#FF9A8B',  # Merah Muda
    'Koolkost': '#FF7F50'     # Oranye Koral Terang
}

# RedDoorz palette (shades) used across charts
reddoorz_palette = [
    "#EB3638",  # primary
    "#C93333",
    "#A22B2B",
    "#8B1F2A",
    "#FF7F50",  # accent (Koolkost)
    "#FF9A8B",
    "#FFD1CF"
]

def make_reddoorz_map(categories):
    cats = list(dict.fromkeys(categories))
    palette = reddoorz_palette
    mapping = {}
    for i, c in enumerate(cats):
        mapping[c] = palette[i % len(palette)]
    return mapping

# For city chart (Q3) we will create a RedDoorz-shade mapping for cities
# Keep city order deterministic for styling
# IMPORTANT: user requested specific mapping for Q3 cities:
# - Yogyakarta -> dark gray
# - Bandung    -> light gray
# - Jakarta    -> Bright Coral Orange (Koolkost / #FF7F50)
# - Malang     -> orange-red
# - Surabaya   -> purple
city_color_map_fixed = {
    'Yogyakarta': '#5a5a5a',     # dark gray (Yogyakarta)
    'Bandung':    '#d9d9d9',     # light gray (Bandung)
    'Jakarta':    '#FF7F50',     # Bright Coral Orange (Jakarta)
    'Malang':     '#FF4500',     # orange-red (Malang)
    'Surabaya':   '#9467bd'      # purple (Surabaya)
}

# --- CUSTOM CSS (unchanged) ---
def style_metric_cards(
    background_color="#FFFFFF",
    border_left_color="#EB3638",
    border_color="#E6E6E6",
    box_shadow=True
):
    box_shadow_css = "box-shadow: 0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24);" if box_shadow else ""
    st.markdown(f"""
    <style>
    /* Normalize box-sizing */
    .stApp, .stApp * {{ box-sizing: border-box; }}

    /* Metric cards base */
    div[data-testid="stMetric"] {{
        background-color: {background_color};
        border: 1px solid {border_color};
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid {border_left_color};
        {box_shadow_css}
        transition: transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .18s ease;
        cursor: default;
    }}

    /* Info box base */
    .info-box {{
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        display: block;
        vertical-align: top;
        min-height: 260px !important;
        height: 100% !important;
        transition: transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .18s ease;
    }}
    .info-title {{
        font-size: 16px;
        font-weight: 700;
        color: #EB3638;
        margin-bottom: 10px;
        text-transform: uppercase;
    }}
    .info-text {{
        font-size: 14px;
        color: #495057;
        line-height: 1.6;
        text-align: justify;
    }}

    /* Ensure the column containers don't add extra spacing that breaks height */
    .stApp .stColumns > div {{
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }}

    /* Safety target our two info-boxes */
    .stApp .block-container .stColumns > div > div {{
        min-height: 260px !important;
    }}

    /* Safety target our two info-boxes */
    .stApp .stColumns > div:nth-child(1) .info-box,
    .stApp .stColumns > div:nth-child(2) .info-box {{
        min-height: 260px !important;
        height: 100% !important;
    }}

    @media (max-width: 900px) {{
        .info-box {{
            min-height: 180px !important;
        }}
    }}

    /* ================
      TABEL STYLING
      ================ */
    table.styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        font-size: 14px;
    }}

    table.styled-table thead th {{
        background-color: #EB3638 !important;
        color: white !important;
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
    }}

    table.styled-table tbody td {{
        padding: 10px;
        border: 1px solid #ddd;
        background-color: white;
    }}

    table.styled-table tbody tr:nth-child(2),
    table.styled-table tbody tr:nth-child(4) {{
        background-color: #f5f5f5 !important;
    }}

    table.styled-table tr:hover td {{
        background-color: #fafafa;
    }}

    /* KPI styling */
    div[data-testid="stMetric"] > div:nth-child(1) {{
        font-weight: 700 !important;
        color: #666666;
    }}
    div[data-testid="stMetric"] > div:nth-child(2) {{
        font-weight: 900 !important;
        font-size: 1.6rem !important;
    }}
    .stMetricValue, .stMetricLabel {{
        font-weight: 900 !important;
    }}

    </style>
    """, unsafe_allow_html=True)

# --- HOVER & INTERACTION CSS ENHANCEMENTS (unchanged) ---
hover_enhancements = """
<style>
div[data-testid="stPlotlyChart"] {
    transition: transform 0.22s cubic-bezier(.2,.8,.2,1), box-shadow 0.22s cubic-bezier(.2,.8,.2,1);
    border-radius: 12px;
}
div[data-testid="stPlotlyChart"]:nth-of-type(1):hover {
    transform: translateY(-10px);
    box-shadow: 0 22px 56px rgba(235,54,56,0.14);
}
div[data-testid="stPlotlyChart"]:nth-of-type(2):hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 48px rgba(0,0,0,0.20);
}
.info-box:hover {
    transform: translateY(-8px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.12);
    cursor: pointer;
}
.info-box:hover .info-title {
    text-decoration: underline;
    text-underline-offset: 6px;
}
table.styled-table tbody tr {
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    transform-origin: left center;
}
table.styled-table tbody tr:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.06);
    cursor: pointer;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.12);
    cursor: pointer;
}
div[data-testid="stMetric"]:hover {
    border-left-width: 8px;
}
div[data-testid="stMetric"]:hover > div:nth-child(1) { font-size: 0.95rem !important; color: #444 !important; }
div[data-testid="stMetric"]:hover > div:nth-child(2) { transform: scale(1.03); }
@media (max-width: 800px) {
    div[data-testid="stPlotlyChart"]:nth-of-type(1):hover,
    div[data-testid="stPlotlyChart"]:nth-of-type(2):hover {
        transform: none; box-shadow: none;
    }
}
</style>
"""

st.markdown(persistent_highlight_css, unsafe_allow_html=True)

# --- 2. FUNGSI LOAD DATA & CACHING (unchanged) ---
@st.cache_data
def load_data():
    try:
        df_bookings = pd.read_csv("Online Budget Hotel Dataset.xlsx - Bookings Table.csv")
        df_property = pd.read_csv("Online Budget Hotel Dataset.xlsx - Property Table.csv")
        df_user = pd.read_csv("Online Budget Hotel Dataset.xlsx - User Table.csv")
        for df in [df_bookings, df_property, df_user]:
            df.drop(columns=[col for col in df.columns if 'Unnamed' in col], inplace=True, errors='ignore')
        df_bookings['CHECK_IN_DATE'] = pd.to_datetime(df_bookings['CHECK_IN_DATE'], errors='coerce')
        df_property['COHORT_DATE'] = pd.to_datetime(df_property['COHORT_DATE'], errors='coerce')
        df_bookings['REVENUE_DOLLAR'] = pd.to_numeric(df_bookings['REVENUE_DOLLAR'], errors='coerce')
        df_bookings['ROOM_NIGHTS'] = pd.to_numeric(df_bookings['ROOM_NIGHTS'], errors='coerce')
        df_property['INVENTORY'] = pd.to_numeric(df_property['INVENTORY'], errors='coerce')
        if 'USER_TYPE' in df_bookings.columns:
            df_bookings['USER_TYPE'] = df_bookings['USER_TYPE'].astype(str).str.strip().str.title()
        if 'USER_TYPE' in df_user.columns:
            df_user['USER_TYPE'] = df_user['USER_TYPE'].astype(str).str.strip().str.title()
        if 'BRAND_TYPE' in df_property.columns:
            df_property['BRAND_TYPE'] = df_property['BRAND_TYPE'].astype(str).str.strip().str.title()
        if 'CITY' in df_property.columns:
            df_property['CITY'] = df_property['CITY'].astype(str).str.strip().str.title()
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

df_main, df_prop_raw = load_data()
if df_main is None:
    st.error("❌ File CSV tidak ditemukan. Pastikan 3 file dataset ada di folder yang sama dengan app.py")
    st.stop()

# --- Validate required columns (unchanged) ---
required_bookings = ['BOOKING_ID','USER_ID','PROPERTY_CODE','CHECK_IN_DATE','ROOM_NIGHTS','REVENUE_DOLLAR','USER_TYPE']
required_property = ['PROPERTY_CODE','BRAND_TYPE','CITY','INVENTORY','COHORT_DATE']
required_user = ['USER_ID','USER_TYPE','USER_GENDER']

missing = []
for c in required_bookings:
    if c not in df_main.columns:
        missing.append(c)
for c in required_property:
    if c not in df_prop_raw.columns:
        missing.append(c)
if missing:
    st.error(f"Kolom wajib hilang: {missing}. Periksa file sumber.")
    st.stop()

# --- 3. SIDEBAR FILTER (small change: removed divider above Grade) ---
st.sidebar.image("https://i0.wp.com/join.reddoorz.com/wp-content/uploads/2022/12/rdlogo.png?fit=960%2C434&ssl=1", width=200)
st.sidebar.divider()
st.sidebar.markdown("## 🔍 Filter Data")

all_brands = sorted(df_main['BRAND_TYPE'].dropna().unique())
selected_brands = st.sidebar.multiselect("🏷️ Pilih Brand:", all_brands, default=all_brands)

all_cities = sorted(df_main['CITY'].dropna().unique())
selected_cities = st.sidebar.multiselect("🏙️ Pilih Kota:", all_cities, default=all_cities)

all_users = sorted(df_main['USER_TYPE'].dropna().unique())
selected_users = st.sidebar.multiselect("👥 Pilih User Type:", all_users, default=all_users)

# divider removed here intentionally to hide the horizontal line above Grade filter
# st.sidebar.divider()

# --- D. Filter Grade (ONLY A-E, remove 'Unknown') ---
# Tampilkan pilihan grade hanya A sampai E (tetap urut A->E)
all_grades = ['A', 'B', 'C', 'D', 'E']

selected_grades = st.sidebar.multiselect(
    "⭐ Filter Kualitas (Grade):",
    options=all_grades,
    default=all_grades
)

# --- B. Filter Tanggal (moved BELOW grade filter as requested) ---
# compute min/max from df_main (safe even if CHECK_IN_DATE has NaT)
min_date = df_main['CHECK_IN_DATE'].min()
max_date = df_main['CHECK_IN_DATE'].max()

start_date, end_date = st.sidebar.date_input(
    "📅 Periode Check-In:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# --- C. Logika Hitung Grade dan property-level aggregation (menggunakan active_days per property) ---
# days_count tetap bisa dipakai untuk fallback/summary tapi kita akan gunakan active_days per property
days_count = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1

# Filter transaksi dalam rentang yang dipilih (unchanged)
temp_df = df_main[
    (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) & 
    (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
]

# Hitung total SOLD (room nights) per property selama periode filter
prop_agg = temp_df.groupby('PROPERTY_CODE').agg(
    SOLD=('ROOM_NIGHTS', 'sum')
).reset_index()

# Ambil property master termasuk COHORT_DATE (kita butuh cohort untuk active days)
active_props_all = df_prop_raw[['PROPERTY_CODE','BRAND_TYPE','CITY','INVENTORY','COHORT_DATE']].copy()
active_props_all['COHORT_DATE'] = pd.to_datetime(active_props_all['COHORT_DATE'], errors='coerce')

# Gabungkan dengan sold
prop_final = pd.merge(active_props_all, prop_agg, on='PROPERTY_CODE', how='left').fillna({'SOLD':0})

# Hitung active_days per property:
# active_start = max(COHORT_DATE, start_date)
# active_end = min(end_date, today) -> kita gunakan end_date karena filter pengguna
start_dt = pd.to_datetime(start_date)
end_dt = pd.to_datetime(end_date)

# If COHORT_DATE is NaT -> treat as start_dt (assume active since filter start)
prop_final['COHORT_DATE'] = prop_final['COHORT_DATE'].fillna(start_dt)

# active_start = max(cohort_date, start_dt)
prop_final['ACTIVE_START'] = prop_final['COHORT_DATE'].apply(lambda d: d if d > start_dt else start_dt)

# active_end = end_dt (we assume property active up to filter end date)
prop_final['ACTIVE_END'] = end_dt

# active_days = (ACTIVE_END - ACTIVE_START).days + 1, minimum 0
prop_final['ACTIVE_DAYS'] = (prop_final['ACTIVE_END'] - prop_final['ACTIVE_START']).dt.days + 1
prop_final.loc[prop_final['ACTIVE_DAYS'] < 0, 'ACTIVE_DAYS'] = 0
prop_final['ACTIVE_DAYS'] = prop_final['ACTIVE_DAYS'].fillna(0).astype(int)

# AVAILABLE now uses per-property active days (safer than global days_count)
prop_final['INVENTORY'] = pd.to_numeric(prop_final['INVENTORY'], errors='coerce').fillna(0).astype(float)
prop_final['AVAILABLE'] = prop_final['INVENTORY'] * prop_final['ACTIVE_DAYS']

# Compute occupancy %
prop_final['OCC'] = 0.0
mask = prop_final['AVAILABLE'] > 0
prop_final.loc[mask, 'OCC'] = (prop_final.loc[mask, 'SOLD'] / prop_final.loc[mask, 'AVAILABLE']) * 100

# Keep previous grade logic (thresholds are the same)
def get_grade_logic(x):
    if x > 80: return 'A'
    elif x >= 70: return 'B'
    elif x >= 40: return 'C'
    elif x >= 20: return 'D'
    else: return 'E'

prop_final['GRADE'] = prop_final['OCC'].apply(get_grade_logic)

# Map grade back to main dataset for downstream filters/charts
grade_mapping = dict(zip(prop_final['PROPERTY_CODE'], prop_final['GRADE']))

# PERBAIKAN ERROR KeyError: 'CURRENT_GRADE'
# Baris yang benar:
df_main['CURRENT_GRADE'] = df_main['PROPERTY_CODE'].map(grade_mapping) 
# Baris yang menyebabkan error (DIHAPUS): df_main['CURRENT_GRADE'] = df_main['CURRENT_GRADE'].map(grade_mapping) 

df_main['CURRENT_GRADE'] = df_main['CURRENT_GRADE'].fillna('Unknown') 

# --- E. Terapkan Semua Filter ke filtered_df (unchanged) ---
filtered_df = df_main[
    (df_main['BRAND_TYPE'].isin(selected_brands)) &
    (df_main['CITY'].isin(selected_cities)) &
    (df_main['USER_TYPE'].isin(selected_users)) &
    (df_main['CURRENT_GRADE'].isin(selected_grades)) &
    (df_main['CHECK_IN_DATE'] >= pd.to_datetime(start_date)) &
    (df_main['CHECK_IN_DATE'] <= pd.to_datetime(end_date))
].copy()

if (prop_final['INVENTORY'] <= 0).any():
    st.warning("Beberapa properti memiliki INVENTORY <= 0. Hasil okupansi/proporsi bisa tidak valid untuk property tersebut.")

# --- 4. KPI UTAMA (Header) (unchanged) ---
st.title("🏨 Dashboard Analisis Bisnis RedDoorz")
st.markdown(f"Periode Analisis: **{start_date}** s/d **{end_date}**")

with st.expander("ℹ️  KONTEKS BISNIS DAN PANDUAN ANALISIS (Klik untuk membuka)", expanded=True):
    style_metric_cards()
    st.markdown(hover_enhancements, unsafe_allow_html=True)
    c1, c2 = st.columns([1,1])
    with c1:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
            <div class="info-title">🎯 TUJUAN BISNIS UTAMA</div>
            <div class="info-text">
            Menganalisis performa operasional dan profitabilitas portofolio RedDoorz untuk:
            <ul style="margin-top: 5px;">
                <li>✅<b>Identifikasi Aset Unggul (Replicate):</b> Meniru strategi properti Grade A.</li>
                <li>⚠️<b>Identifikasi Aset Lemah (Fix):</b> Memperbaiki atau delisting properti Grade E.</li>
            </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
            <div class="info-title">🏨 PROFIL BRAND</div>
            <div class="info-text">
            <b>1. RedDoorz (Core):</b><br>Harian, Budget, Wisatawan/Bisnis Singkat. Fasilitas standar.<br><br>
            <b>2. KoolKost (Co-Living):</b><br>Jangka Panjang (>7 hari), Kost, Mahasiswa/Pekerja. Low margin, High stability.<br><br>
            <b>3. RedPartner (Mitra):</b><br>Kemitraan lokal (Guesthouse), dikelola mitra, variatif.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-title" style="margin-top: 20px;">📊 PANDUAN VISUALISASI & PERTANYAAN BISNIS</div>
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
                <td>Mendiagnosis proporsi aset yang "Sehat" (Grade A) vs "Sakit" (Grade E) dalam portofolio.</td>
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

style_metric_cards()

col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_df['REVENUE_DOLLAR'].sum()
total_bookings = filtered_df['BOOKING_ID'].nunique()
total_nights = filtered_df['ROOM_NIGHTS'].sum()
avg_adr = total_revenue / total_nights if total_nights > 0 else 0

repeat_user_count = filtered_df[filtered_df['USER_TYPE'].str.lower() == 'repeat user']['USER_ID'].nunique()
total_unique_users = filtered_df['USER_ID'].nunique()
retention_rate = (repeat_user_count / total_unique_users * 100) if total_unique_users > 0 else 0

# Format angka lengkap untuk ditampilkan di dalam Tooltip
real_revenue = f"${total_revenue:,.2f}"
real_bookings = f"{total_bookings:,}"
real_nights = f"{total_nights:,}"
real_adr = f"${avg_adr:,.2f}"
real_retention = f"{retention_rate:.2f}%"

# Logika format singkat (M / K) untuk tampilan utama (TETAP SAMA)
if total_revenue >= 1_000_000:
    formatted_revenue = f"${total_revenue/1_000_000:.2f} M"
elif total_revenue >= 1_000:
    formatted_revenue = f"${total_revenue/1_000:.2f} K"
else:
    formatted_revenue = f"${total_revenue:,.2f}"

# --- MENAMPILKAN METRIC DENGAN TOOLTIP DINAMIS ---
with col1:
    st.metric(
        "Total Revenue", 
        formatted_revenue, 
        # Di sini kita masukkan nilai asli (real_revenue) ke dalam tooltip
        help=f"💰 Nilai Lengkap: {real_revenue}\n\nTotal pendapatan dalam periode terpilih."
    )
with col2:
    st.metric(
        "Total Transaksi", 
        f"{total_bookings:,}", # Tampilan utama (mungkin kepotong CSS)
        help=f"🧾 Nilai Lengkap: {real_bookings}\n\nJumlah Booking ID Unik yang tercatat."
    )
with col3:
    st.metric(
        "Room Nights", 
        f"{total_nights:,}", 
        help=f"🛏️ Nilai Lengkap: {real_nights}\n\nTotal malam kamar terjual."
    )
with col4:
    st.metric(
        "Avg ADR", 
        f"${avg_adr:,.2f}", 
        help=f"🏷️ Nilai Lengkap: {real_adr}\n\nAverage Daily Rate (Rata-rata harga per malam)."
    )
with col5:
    st.metric(
        "Retention Rate", 
        f"{retention_rate:.1f}%", 
        help=f"👥 Nilai Lengkap: {real_retention}\n\nPersentase user unik yang melakukan transaksi lebih dari sekali (Repeat User)."
    )

st.divider()

# --- 5. TABS ANALISIS ---
# Mengubah baris tabs untuk menambahkan Tab 4 di posisi yang diinginkan
tab1, tab2, tab3, tab4 = st.tabs(["📊 1. Aset & Kualitas", "🗺️ 2. Wilayah & Revenue", "👥 3. Pelanggan & Loyalitas", "⭐ 4. Rangkuman Aksi Strategis"])

# TAB 1: Aset & Kualitas (Q1 & Q4)
with tab1:
    st.subheader("Q1: Komposisi Performa Okupansi Properti (Grade A-E)")
    
    # --- PERBAIKAN DI SINI ---
    # Tambahkan filter: (prop_final['GRADE'].isin(selected_grades))
    pf_filtered = prop_final[
        (prop_final['BRAND_TYPE'].isin(selected_brands)) &
        (prop_final['CITY'].isin(selected_cities)) &
        (prop_final['GRADE'].isin(selected_grades))  # <--- INI YANG KURANG
    ].copy()
    # -------------------------

    grade_dist = pf_filtered['GRADE'].value_counts().reset_index()
    grade_dist.columns = ['GRADE','COUNT']
    grade_dist = grade_dist.sort_values('GRADE', key=lambda s: s.map({'A':0,'B':1,'C':2,'D':3,'E':4}))

    # Use reddoorz palette for grade slices (A-E)
    reddoorz_grade_map = make_reddoorz_map(['A','B','C','D','E'])

    st.markdown("<div class='chart-hover'>", unsafe_allow_html=True)

    # --- NEW: compute percent and smarter pull values for small slices ---
    total = grade_dist['COUNT'].sum() if grade_dist['COUNT'].sum() > 0 else 1
    grade_dist['PCT'] = grade_dist['COUNT'] / total

    pulls = []
    for pct in grade_dist['PCT']:
        # increase pull for very small slices so they separate and become visible
        if pct < 0.06:
            pulls.append(0.20)    # very small -> pull out strongly
        elif pct < 0.12:
            pulls.append(0.10)    # small -> moderate pull
        else:
            pulls.append(0.0)     # large slices no pull

    # Slightly reduce hole to give more ring thickness (labels outside clearer)
    # Slightly reduce hole to give more ring thickness (labels outside clearer)
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

    # Increase side margins so small slices + legend have space and don't overlap
    fig_q1.update_layout(
        margin=dict(t=10, b=160, l=40, r=140),
        height=520,
        autosize=True,
        showlegend=True,
        legend=dict(orientation="v", y=0.55, x=0.02, title="Grade", font=dict(size=11))
    )

    st.plotly_chart(fig_q1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    brand_counts = pf_filtered.groupby('BRAND_TYPE')['PROPERTY_CODE'].nunique().rename('TOTAL_PROPERTY')
    grade_e_counts = pf_filtered[pf_filtered['GRADE']=='E'].groupby('BRAND_TYPE')['PROPERTY_CODE'].nunique().rename('E_COUNT')
    brand_summary = pd.concat([brand_counts, grade_e_counts], axis=1).fillna(0)
    brand_summary['E_PROP'] = brand_summary['E_COUNT'] / brand_summary['TOTAL_PROPERTY']
    brand_summary = brand_summary.sort_values('E_PROP', ascending=False).reset_index()

    st.markdown("**Brand breakdown (proporsi Grade E)**")
    st.dataframe(brand_summary.style.format({'E_PROP':'{:.1%}','TOTAL_PROPERTY':'{:.0f}','E_COUNT':'{:.0f}'}))

    # >>>>>> INSIGHT Q1 <<<<<<
    st.info("""
    **Temuan Kritis** 🚨: $\mathbf{95.4\%}$ aset berada di **Grade E** (<20% Okupansi), krisis merata di semua brand. Properti unggul (A/B) hanya 0.8%. **RedPartner** ($\mathbf{95.8\%}$) memiliki proporsi E tertinggi.
    **Rekomendasi Strategi**: 1) **Delisting** agresif pada Grade E terburuk (fokus RedPartner). 2) **Fokus perbaikan** intensif hanya pada Grade C/D ($\sim 4\%$) untuk peningkatan cepat. 3) **Kloning** praktik operasional dari 3 properti Grade A.
    """)
    # >>>>>> END INSIGHT Q1 <<<<<<

    st.markdown("<br/>", unsafe_allow_html=True)

    # Q4: Tren Akuisisi (use brand color map)
    st.subheader("Q4: Tren Akuisisi Properti Baru (Tahunan)")
    df_cohort = df_prop_raw[df_prop_raw['BRAND_TYPE'].isin(selected_brands)].copy()
    df_cohort['YEAR'] = df_cohort['COHORT_DATE'].dt.year
    yearly_growth = df_cohort.groupby(['YEAR','BRAND_TYPE']).size().reset_index(name='NEW_PROPERTIES')

    # Use brand color map (RedDoorz theme) for Q4 lines -- UPDATED to use color_map_brand
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
    
    # >>>>>> INSIGHT Q4 <<<<<<
    st.info("""
    **Temuan Kritis** 🚨: **RedDoorz** ($46$ unit di 2022) dan **KoolKost** ($43$ unit di 2023) adalah *driver* pertumbuhan kuantitas yang agresif. Temuan ini **bertolak belakang dengan Q1**, menunjukkan akuisisi memprioritaskan **volume di atas kualitas aset**.
    **Rekomendasi Strategi**: 1) **Moratorium Akuisisi RedPartner**: Alihkan modal dari akuisisi RedPartner ke **perbaikan aset Grade C/D** yang ada untuk peningkatan kinerja yang pasti. 2) **Ubah Metrik BD (Business Development)**: Ukur tim akuisisi TIDAK dari *jumlah* aset baru, tetapi dari **persentase properti baru yang mencapai Grade C dalam 6 bulan**.
    """)
    # >>>>>> END INSIGHT Q4 <<<<<<

# TAB 2: Wilayah & Revenue (Q3)
with tab2:
    st.subheader("Q3: Peringkat Kota Berdasarkan Revenue")
    city_agg = filtered_df.groupby('CITY').agg(
        TOTAL_REVENUE=('REVENUE_DOLLAR','sum'),
        TOTAL_SOLD=('ROOM_NIGHTS','sum')
    ).reset_index()

    # Buat city-level available menggunakan AVAILABLE yang telah dikalkulasi per property
    # Ambil AVAILABLE dari prop_final untuk properties yang ada di filtered_df (respect brand/city filter)
    city_available = prop_final.groupby('CITY')['AVAILABLE'].sum().reset_index().rename(columns={'AVAILABLE':'CITY_AVAILABLE'})

    # Merge untuk menghasilkan df_city yang komprehensif
    df_city = pd.merge(city_agg, city_available, on='CITY', how='left')
    df_city['CITY_AVAILABLE'] = df_city['CITY_AVAILABLE'].fillna(0)

    # ADR unchanged
    df_city['ADR'] = df_city.apply(lambda r: (r['TOTAL_REVENUE']/r['TOTAL_SOLD']) if r['TOTAL_SOLD'] and r['TOTAL_SOLD']>0 else 0, axis=1)

    # OCC_RATE now uses city-level available (inventory * active_days)
    df_city['OCC_RATE'] = df_city.apply(lambda r: (r['TOTAL_SOLD'] / r['CITY_AVAILABLE']) if r['CITY_AVAILABLE']>0 else 0, axis=1)
    df_city['OCCUPANCY'] = df_city['OCC_RATE'] * 100
    df_city['REVPAR'] = df_city['ADR'] * df_city['OCC_RATE']

    df_city_sorted = df_city.sort_values('TOTAL_REVENUE', ascending=False)
    df_city_sorted['K_format'] = (df_city_sorted['TOTAL_REVENUE'] / 1000).round().astype(int).astype(str) + "k"

    # Build mapping using fixed city color map for requested cities.
    # If a city not in fixed map appears, fallback to reddoorz_palette sequence.
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
    fig_q3.update_layout(xaxis={'categoryorder':'total descending'}, bargap=0.22, hoverlabel=dict(bgcolor="white",font_color="black"), legend_title_text='Kota', margin=dict(t=40,b=40,l=40,r=20), yaxis_tickformat='.0s')
    st.plotly_chart(fig_q3, use_container_width=True)

    st.markdown("**Tabel ringkasan per-kota (Total Revenue, ADR, Okupansi, dan RevPAR)**")
    st.dataframe(df_city_sorted[['CITY','TOTAL_REVENUE','ADR','OCCUPANCY','REVPAR']].sort_values('TOTAL_REVENUE', ascending=False).style.format({'TOTAL_REVENUE':'{:.0f}','ADR':'{:.2f}','OCCUPANCY':'{:.2f}','REVPAR':'{:.2f}'}))

    # >>>>>> INSIGHT Q3 <<<<<<
    # Teks telah diperbaiki untuk menghilangkan simbol LaTeX yang menyebabkan error rendering:
    st.info("""
    **Temuan Kritis** 🗺️: **Yogyakarta** adalah mesin revenue utama (**\$427K**) yang didorong oleh **Okupansi tertinggi** (1.61%). **ADR Seragam** (sekitar **\$5.00**) di semua kota menunjukkan pendapatan TIDAK didorong harga. Seluruh pasar menderita krisis volume yang parah (RevPAR sangat rendah).
    **Rekomendasi Strategi**: 1) **Monetisasi Yogyakarta/Jakarta**: Segera uji ADR naik **\$0.50** di properti Grade C/D di Yogyakarta dan Jakarta, karena permintaan volume terbukti ada. 2) **Fokus Volume**: Alokasikan *marketing* agresif untuk meningkatkan Okupansi di **Bandung, Malang, dan Surabaya** (pasar yang tertinggal).
    """)
    # >>>>>> END INSIGHT Q3 <<<<<<

# TAB 3: Pelanggan (Q2 & Q5)
with tab3:
    st.subheader("Q2: Perbandingan Harga (ADR) per Brand")

    brand_perf = filtered_df.groupby('BRAND_TYPE').agg(REV=('REVENUE_DOLLAR','sum'), RN=('ROOM_NIGHTS','sum')).reset_index()
    brand_perf['ADR'] = brand_perf.apply(lambda r: (r['REV']/r['RN']) if r['RN'] and r['RN']>0 else 0, axis=1)

    # Use brand color map (RedDoorz colors) for Q2 bars -- UPDATED to use color_map_brand
    brands_present = brand_perf['BRAND_TYPE'].tolist()
    final_brand_map = {}
    for i,b in enumerate(brands_present):
        final_brand_map[b] = color_map_brand.get(b, reddoorz_palette[i % len(reddoorz_palette)])

    brand_perf['TEXT'] = brand_perf['ADR'].apply(lambda x: f"{x:.2f}")
    fig_q2 = px.bar(
        brand_perf, x='BRAND_TYPE', y='ADR', color='BRAND_TYPE',
        color_discrete_map=final_brand_map, text='TEXT',
        labels={'ADR':'Rata-rata Harga ($)','BRAND_TYPE':'Brand'},
        hover_data={'REV':':,.0f','RN':':,.0f','ADR':':.2f','BRAND_TYPE':False}
    )
    fig_q2.update_traces(textposition='outside', marker_line_width=1, marker_line_color='rgba(0,0,0,0.08)')
    fig_q2.update_layout(yaxis_range=[0, max(brand_perf['ADR'].max()*1.15, 6)], uniformtext_minsize=10, uniformtext_mode='hide', showlegend=True, legend_title_text='Brand', margin=dict(t=30,b=20,l=40,r=20))
    fig_q2.update_yaxes(tickformat='.2f')
    st.plotly_chart(fig_q2, use_container_width=True)
    
    # >>>>>> INSIGHT Q2 <<<<<<
    # Teks telah diperbaiki untuk menghilangkan simbol LaTeX yang menyebabkan error rendering:
    st.info("""
    **Temuan Kritis** ⚠️: ADR sangat seragam (sekitar **\$5.00**) di semua brand (**RedDoorz: \$5.00, KoolKost: \$4.98, RedPartner: \$5.00**). Keseragaman ini menunjukkan **kegagalan diferensiasi nilai produk**. **KoolKost** gagal memberikan insentif harga (*ADR long-stay* seharusnya jauh lebih rendah).
    **Rekomendasi Strategi**: 1) Terapkan **diskon volume wajib** (**15% - 20%** lebih rendah) pada KoolKost untuk durasi inap panjang. 2) **Uji kenaikan harga agresif** di properti **Grade A** (Okupansi > 80%) menuju ADR **\$6.00** untuk membuktikan *pricing power* aset unggul.
    """)
    # >>>>>> END INSIGHT Q2 <<<<<<

    st.markdown("<br/>", unsafe_allow_html=True)

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

        # Custom Color Map for A and E: Red and Orange
        reddoorz_grade_map_ae = {
            'A': '#EB3638',  # Merah (primary)
            'E': '#FF7F50'   # Oranye Koral (Koolkost / accent)
        }
        
        fig_q5 = px.bar(
            loyalty_final, x='CURRENT_GRADE', y='REPEAT_RATIO',
            # Menggunakan color_discrete_map yang sudah didefinisikan secara spesifik
            color='CURRENT_GRADE', color_discrete_map=reddoorz_grade_map_ae,
            text_auto='.1%', labels={'CURRENT_GRADE':'Grade Properti','REPEAT_RATIO':'Proporsi Repeat User'}
        )
        fig_q5.update_traces(textposition='outside')
        fig_q5.update_layout(
            yaxis_title="Proporsi Repeat User", 
            yaxis=dict(tickformat=".0%"), 
            showlegend=True, # Mengaktifkan legend
            legend_title_text="Grade", # Menambah judul legend
            margin=dict(t=20,b=20,l=20,r=20), 
            height=300, 
            yaxis_range=[0,1]
        )
        st.plotly_chart(fig_q5, use_container_width=True)

        st.markdown("**Tabel proporsi Repeat User per Grade (A vs E)**")
        st.dataframe(loyalty_final.style.format({'REPEAT_RATIO':'{:.1%}'}))

        # Attempt chi-square test only if scipy is present.
        # If scipy is not installed, fail silently (no message shown).
        # try:
        #     from scipy.stats import chi2_contingency
        #     ct = pd.crosstab(subset_loyalty['CURRENT_GRADE'], subset_loyalty['USER_TYPE']=='Repeat User')
        #     if ct.shape == (2,2):
        #         chi2, p, dof, expected = chi2_contingency(ct)
        #         st.write("Chi-square p-value:", f"{p:.4f}")
        #         if p < 0.05:
        #             st.success("Perbedaan proporsi Repeat User antara Grade A dan E signifikan (p < 0.05).")
        #         else:
        #             st.info("Tidak ada bukti signifikan perbedaan proporsi Repeat User antara Grade A dan E.")
        #     else:
        #         st.info("Data tidak cocok untuk uji Chi-square (kontingensi bukan 2x2).")
        # except Exception:
        #     # scipy not available or test failed -> skip silently (no message)
        #     pass

        # >>>>>> INSIGHT Q5 <<<<<<
        st.info("""
        **Temuan Kritis** 👥: Proporsi **Repeat User** di Grade A (49.2%) hanya sedikit lebih tinggi (2%) dari Grade E (47.2%). Perbedaan ini **terlalu kecil** untuk memvalidasi ROI kualitas aset secara kuat.
        **Rekomendasi Strategi**: 1) **Audit Kualitas Pengalaman (QoE)** properti Grade A (Okupansi tinggi) untuk mengidentifikasi dan mereplikasi *unique selling points* yang benar-benar menciptakan loyalitas. 2) **Re-evaluasi metrik Grade** untuk memasukkan *Rating* atau *NPS* agar Grade A benar-benar mencerminkan kualitas superior.
        """)
        # >>>>>> END INSIGHT Q5 <<<<<<
    else:
        st.warning("Data tidak cukup untuk membandingkan Grade A dan Grade E pada filter yang dipilih.")

# --- 6. TAMBAH TAB 4 (RANGKUMAN EKSEKUTIF) ---
with tab4:
    st.subheader("⭐ Rangkuman Aksi Strategis Portofolio")
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

    st.markdown("### 🎯 Rekomendasi Prioritas Berdasarkan Tujuan Bisnis Utama (Q1 - Q5)")
    
    # Data Konsolidasi dari Q1-Q5 (Dikonversi ke string yang aman)
    data_summary = [
        # Q1 & Q4 - Kualitas Aset & Ekspansi
        {
            'Aspek': 'Kualitas Aset & Konsolidasi',
            'Temuan Kritis': '🚨 **95.4%** aset adalah **Grade E** (krisis volume). Ekspansi agresif RedPartner/KoolKost menambah volume aset berkinerja buruk.',
            'Aksi Rekomendasi': 'Fokus **Delisting Agresif** properti E yang terburuk. Alihkan modal ke **Perbaikan Intensif aset Grade C/D** (aset potensial ~4%). Tim BD diukur berdasarkan **kualitas (Grade C/B)**, bukan volume akuisisi mentah.',
            'Konteks': 'Q1, Q4'
        },
        # Q2 & Q3 - Revenue Management & Pricing Power
        {
            'Aspek': 'Pricing & Revenue Management',
            'Temuan Kritis': '⚠️ **ADR Seragam** (sekitar $5.00) di semua *brand* dan kota (**Q2**), menunjukkan **kegagalan diferensiasi nilai**. KoolKost tidak memberikan insentif harga *long-stay*.',
            'Aksi Rekomendasi': 'Terapkan **diskon volume wajib (15%–20%)** untuk KoolKost. Segera uji kenaikan ADR ($+0.50) di properti Grade C/D di pasar terkuat (**Yogyakarta/Jakarta**) untuk membangun *pricing power* yang hilang.',
            'Konteks': 'Q2, Q3'
        },
        # Q5 - Loyalitas Pelanggan
        {
            'Aspek': 'Loyalitas & Pengalaman Pelanggan (QoE)',
            'Temuan Kritis': '👥 Korelasi loyalitas sangat lemah: Grade A hanya 2% Repeat User lebih tinggi dari Grade E. Okupansi tinggi TIDAK secara otomatis berarti kualitas pengalaman superior.',
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
        # 1. Bersihkan LaTeX (Kode lama Anda)
        raw_krit = item['Temuan Kritis'].replace(r'\mathbf{', '').replace('}', '').replace(r'\sim', '~').replace(r'\mathbf', '').replace(r'\$', '$')
        raw_aksi = item['Aksi Rekomendasi'].replace(r'\mathbf{', '').replace('}', '').replace(r'\$', '$')

        # 2. KONVERSI MARKDOWN KE HTML (Baris Baru)
        
        # Langkah A: Ubah **teks** menjadi <b>teks</b> (Bold)
        krit_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_krit)
        aksi_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_aksi)

        # Langkah B: Ubah *teks* menjadi <i>teks</i> (Italic)
        krit_html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', krit_html)
        aksi_html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', aksi_html)

        # 3. Masukkan ke dalam Tabel HTML (Tanpa indentasi agar tidak jadi code block)
        html_table += f"""
<tr>
    <td style="font-weight: 700; color: #8B0000;">{item['Aspek']}</td>
    <td>{krit_html}</td>
    <td style="font-style: italic;">{aksi_html}</td>
</tr>
"""
    html_table += "</tbody></table>"

    st.markdown(html_table, unsafe_allow_html=True)


# --- 6. FOOTER (unchanged) ---
footer_css = """
<style>
.footer-container {
    background: transparent;
    padding: 18px 12px;
    border-radius: 10px;
    text-align: center;
    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #333333;
    margin-top: 170px;
    border-top: 3px solid #EB3638;
    padding-top: 30px;
}
.footer-container .sponsor {
    color: #666666;
    font-size: 14px;
    margin-bottom: 6px;
}
.footer-container h2 {
    color: #EB3638 !important;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 0;
    font-size: 20px;
    display: inline-block;
    padding: 8px 14px;
    border-radius: 14px;
    box-shadow: 0 26px 60px rgba(235,54,56,0.10), inset 0 1px 0 rgba(255,255,255,0.2);
    transform: translateY(-4px);
    transition: transform 0.35s ease, box-shadow 0.35s ease;
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
.team-badge {
    padding: 8px 18px;
    border-radius: 24px;
    color: white;
    font-weight: 700;
    font-size: 14px;
    display: inline-block;
    margin: 6px;
    background-image: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(0,0,0,0.02));
    box-shadow: 0 18px 40px rgba(0,0,0,0.10), 0 6px 18px rgba(0,0,0,0.06);
    transform: translateY(-3px);
    transition: transform 0.35s ease, box-shadow 0.35s ease;
    text-shadow: 0 1px 0 rgba(0,0,0,0.18);
}
@keyframes float-subtle {
    0% { transform: translateY(-3px); }
    50% { transform: translateY(-1px); }
    100% { transform: translateY(-3px); }
}
.team-badge { animation: float-subtle 4.5s ease-in-out infinite; }
.team-badge[style*="#EB3638"] { background-color: #EB3638; color: white; }
.team-badge[style*="#FF7F50"] { background-color: #FF7F50; color: white !important; text-shadow: 0 1px 0 rgba(0,0,0,0.22); }
.team-badge[style*="#8B0000"] { background-color: #8B0000; color: white; }
@media (max-width: 600px) {
    .footer-container h2 { font-size: 18px; padding: 6px 10px; transform: translateY(0); box-shadow: 0 12px 28px rgba(235,54,56,0.08); }
    .team-badge { padding: 6px 12px; font-size: 13px; animation-duration: 5.5s; }
}
.footer-container .copyright { color: #999999; font-size: 12px; margin-top: 18px; }
</style>
"""

footer_html = """
<div class="footer-container">
  <div class="sponsor">Dashboard ini dipersembahkan oleh:</div>
  <h2>📊 SAFARI DATA 🐱</h2>

  <div class="team">
    <span class="team-badge" style="background:#EB3638;">👩🏻‍💻 Nabila Putri Asy Syifa</span>
    <span class="team-badge" style="background:#FF7F50;">🧑🏻‍💻 Farrel Paksi Aditya</span>
    <span class="team-badge" style="background:#8B0000;">👩🏻‍💻 Nur Salamah Azzahrah</span>
  </div>

  <div class="copyright">© 2024 Proyek Akhir Visualisasi Data | RedDoorz Analysis</div>
</div>
"""

html_full = footer_css + textwrap.dedent(footer_html)
st.markdown(html_full, unsafe_allow_html=True)
st.markdown(hover_enhancements, unsafe_allow_html=True)