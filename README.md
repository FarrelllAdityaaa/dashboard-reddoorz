# 🏨 RedDoorz Portfolio Performance Dashboard

<div align="center">

![RedDoorz Logo](https://i0.wp.com/join.reddoorz.com/wp-content/uploads/2022/12/rdlogo.png?fit=960%2C434&ssl=1)

**Dashboard Analisis Bisnis untuk Optimasi Portofolio Properti RedDoorz**

[![Live Demo](https://img.shields.io/badge/Demo-Live-success?style=for-the-badge)](https://dashboard-reddoorz-analysis.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

</div>

---

## 📊 Tentang Proyek

Dashboard interaktif untuk menganalisis **performa operasional dan profitabilitas** portofolio properti RedDoorz di 5 kota utama Indonesia (Jakarta, Bandung, Yogyakarta, Malang, Surabaya).

### 🎯 **Business Problem**

RedDoorz menghadapi tantangan dalam mengelola portofolio properti yang terdiri dari 3 brand berbeda:
- **RedDoorz** (Core Business) - Hotel budget harian
- **KoolKost** (Co-Living) - Kost jangka panjang
- **RedPartner** (Partnership) - Mitra lokal

Dashboard ini membantu stakeholder untuk:
- **Mengidentifikasi aset unggul** untuk direplikasi strateginya
- **Mendeteksi aset bermasalah** untuk delisting atau perbaikan
- **Mengoptimalkan revenue** melalui pricing dan occupancy strategy
- **Meningkatkan customer retention** berbasis analisis loyalitas

---

## 🎯 Tujuan Bisnis

Dashboard ini menjawab **5 Pertanyaan Bisnis Kritis**:

| Kode | Pertanyaan Bisnis | Metrik Kunci | Tujuan |
|------|-------------------|--------------|--------|
| **Q1** | Bagaimana komposisi kualitas aset dalam portofolio? | Distribusi Grade A-E (berdasarkan okupansi) | Identifikasi proporsi aset "sehat" vs "sakit" |
| **Q2** | Apakah strategi pricing efektif untuk setiap brand? | Average Daily Rate (ADR) per brand | Evaluasi diferensiasi nilai produk |
| **Q3** | Kota mana yang menjadi revenue driver utama? | Total Revenue, ADR, Okupansi, RevPAR | Alokasi marketing & expansion strategy |
| **Q4** | Bagaimana tren pertumbuhan akuisisi properti? | Jumlah properti baru per tahun per brand | Evaluasi strategi ekspansi: kualitas vs kuantitas |
| **Q5** | Apakah kualitas properti berkorelasi dengan loyalitas? | Repeat User Rate per Grade | Validasi ROI investasi kualitas aset |

---

## 📈 Analisis Bisnis

### **Q1: Komposisi Performa Okupansi Properti (Grade A-E)**

**Metodologi Grading:**
```
Grade A: Okupansi > 80%  (Excellent)
Grade B: Okupansi 70-80% (Good)
Grade C: Okupansi 40-70% (Average)
Grade D: Okupansi 20-40% (Below Average)
Grade E: Okupansi < 20%  (Critical)
```

**Finding Kritis:**
- **95.4%** properti berada di **Grade E** (krisis okupansi masif)
- Hanya **0.8%** properti mencapai Grade A/B
- **RedPartner** memiliki proporsi Grade E tertinggi (95.8%)

**Business Impact:**
> Mayoritas aset tidak menghasilkan revenue optimal. Diperlukan konsolidasi portofolio untuk fokus pada aset potensial.

---

### **Q2: Perbandingan Harga (ADR) per Brand**

**Key Metrics:**
- **RedDoorz ADR**: $5.00
- **KoolKost ADR**: $4.98
- **RedPartner ADR**: $5.00

**Finding Kritis:**
- **ADR seragam** di semua brand (~$5.00)
- **Kegagalan diferensiasi nilai produk**
- KoolKost tidak memberikan **diskon long-stay** yang seharusnya

**Business Impact:**
> Tidak ada pricing power. Brand gagal menciptakan unique value proposition yang justify perbedaan harga.

---

### **Q3: Peringkat Kota Berdasarkan Revenue**

**Top Cities by Revenue:**
1. 🥇 **Yogyakarta** - $427K (Okupansi 1.61%)
2. 🥈 **Jakarta** - $254K (Okupansi 0.89%)
3. 🥉 **Bandung** - $119K (Okupansi 0.41%)

**Finding Kritis:**
-  **Yogyakarta** adalah revenue engine utama
-  Revenue didorong oleh **volume (okupansi)**, bukan harga
-  ADR seragam $5.00 di semua kota (no premium pricing)

**Business Impact:**
> Opportunity untuk premium pricing di kota high-demand (Yogyakarta, Jakarta). Kota lain butuh marketing boost untuk volume.

---

### **Q4: Tren Pertumbuhan Properti Baru (Tahunan)**

**Ekspansi Agresif:**
- **2022**: RedDoorz menambah **46 unit** (puncak ekspansi)
- **2023**: KoolKost menambah **43 unit**
- **Trend**: Fokus pada **kuantitas akuisisi**

**Finding Kritis:**
-  **Ekspansi volume tinggi** bertolak belakang dengan **kualitas rendah** (Q1)
-  Akuisisi RedPartner tidak menghasilkan aset berkualitas
-  Tidak ada korelasi antara jumlah akuisisi dengan peningkatan Grade

**Business Impact:**
> Strategi ekspansi perlu pivot dari "volume" ke "quality". Moratorium akuisisi brand underperforming diperlukan.

---

### **Q5: Proporsi Loyalitas (Grade A vs Grade E)**

**Repeat User Rate:**
- **Grade A**: 49.2%
- **Grade E**: 47.2%
- **Selisih**: Hanya **2%**

**Finding Kritis:**
-  **Korelasi loyalitas sangat lemah**
-  Okupansi tinggi ≠ Pengalaman superior
-  Grade A tidak membuktikan ROI kualitas aset

**Business Impact:**
> Metrik Grade perlu re-evaluasi. Ocupancy saja tidak cukup untuk mengukur kualitas pengalaman pelanggan (QoE).

---

## 🔍 Key Findings

### 🚨 **Crisis Indicators**

1. **Portfolio Crisis**
   - 95.4% aset di Grade E (volume crisis)
   - Hanya 0.8% aset mencapai performa excellent

2. **Pricing Failure**
   - ADR seragam $5.00 (no differentiation)
   - KoolKost gagal pricing strategy long-stay

3. **Quality vs Quantity Paradox**
   - Ekspansi agresif (46-43 unit/tahun)
   - Tidak ada korelasi dengan peningkatan kualitas

4. **Loyalty Paradox**
   - Grade A vs E hanya beda 2% Repeat User
   - Okupansi tinggi tidak guarantee loyalitas

---

## 💡 Rekomendasi Strategis

### 🎯 **Prioritas 1: Konsolidasi Portofolio**

**Aksi Segera:**
- 🔴 **Delisting Agresif**: Close 30-40% properti Grade E terburuk (fokus RedPartner)
- 🟡 **Intensive Improvement**: Fokus sumber daya pada Grade C/D (~4% portofolio) yang potensial naik
- 🟢 **Best Practice Cloning**: Replikasi strategi operasional dari 3 properti Grade A

**Expected Impact:**
- Reduce operational cost 25-30%
- Increase average portfolio occupancy 40-50%
- Improve brand perception

---

### 💰 **Prioritas 2: Revenue Management Overhaul**

**Pricing Strategy:**
1. **KoolKost Discounting**
   - Implementasi **15-20% discount** untuk long-stay (>7 hari)
   - Target: Increase LTV dan occupancy stability

2. **Premium Pricing Test**
   - **Yogyakarta & Jakarta**: Test ADR increase $0.50 di properti Grade C/D
   - Validasi pricing power di market high-demand

3. **Dynamic Pricing**
   - Implement yield management berdasarkan demand pattern
   - Target: Increase RevPAR 15-20%

**Expected Impact:**
- Revenue increase 10-15% tanpa volume tambahan
- Better product differentiation

---

### 📊 **Prioritas 3: Quality Metrics Redefinition**

**Re-evaluasi Grading System:**
-  **Current**: Hanya okupansi
-  **New**: Okupansi + Rating + NPS + Repeat Rate

**Quality Experience (QoE) Audit:**
- Deep-dive audit properti Grade A
- Identifikasi unique selling points yang drive loyalty
- Standardize best practices

**Expected Impact:**
- Grade A truly reflects superior experience
- Clear ROI untuk quality investment

---

### 🚀 **Prioritas 4: Expansion Strategy Reset**

**Moratorium & Pivot:**
1. **Stop**: Akuisisi RedPartner (95.8% Grade E)
2. **Redirect**: Modal ke improvement Grade C/D existing assets
3. **New Metrics**: BD team measured by "% new properties reaching Grade C in 6 months"

**Expected Impact:**
- Higher quality acquisitions
- Better capital efficiency
- Sustainable growth

---

## 📊 Business Metrics Dashboard

### **Current State (Baseline)**
| Metric | Value | Status |
|--------|-------|--------|
| Grade E Properties | 95.4% | 🔴 Critical |
| Average ADR | $5.00 | 🟡 Below Market |
| Average Occupancy | <20% | 🔴 Critical |
| Repeat User Rate | ~48% | 🟡 Average |
| Revenue Concentration | 63% (Yogyakarta+Jakarta) | 🟡 High Risk |

### **Target State (12 Months)**
| Metric | Target | Growth |
|--------|--------|--------|
| Grade E Properties | <70% | ⬇️ -25% |
| Grade C+ Properties | >20% | ⬆️ +15% |
| Average ADR | $5.50-6.00 | ⬆️ +10-20% |
| Average Occupancy | 30-40% | ⬆️ +15-20% |
| Repeat User Rate | 55-60% | ⬆️ +10% |

---

## Metodologi

### **Data Sources**
- Bookings Transaction Data (2019-2024)
- Property Master Data (Inventory, Cohort, Brand)
- User Profile Data (Type, Gender)

### **Analysis Framework**
- **Descriptive Analytics**: Current state assessment
- **Diagnostic Analytics**: Root cause identification
- **Prescriptive Analytics**: Actionable recommendations

### **Key Assumptions**
- Occupancy sebagai proxy utama performa aset
- ADR sebagai proxy pricing power
- Repeat User sebagai proxy loyalty

---

## 👥 Tim Safari Data

<div align="center">

### **Contributors**

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/FarrelllAdityaaa.png" width="100px;" alt="Farrel Paksi Aditya"/><br />
      <sub><b>Farrel Paksi Aditya</b></sub><br />
      <sub>🧑🏻‍💻 Data Analyst & Business Analyst</sub>
    </td>
    <td align="center">
      <img src="https://github.com/NabilaaaPutriii.png" width="100px;" alt="Nabila Putri Asy Syifa"/><br />
      <sub><b>Nabila Putri Asy Syifa</b></sub><br />
      <sub>🧑🏻‍💻 Data Analyst & Business Analyst</sub>
    </td>
  </tr>
</table>

**Proyek Data Analyst Hotel Reddoorz - 2025**

</div>

---

## 📞 Kontak

-  Email: nabilaputriasysyifa99@gmail.com
-  Linkedln: [Linkedln Account Nabila](www.linkedin.com/in/nabila-putri-asy-syifa)
-  Linkedln: [Linkedln Account Farrel](https://www.linkedin.com/in/farrel-paksi-aditya/)

---

## Acknowledgments

Terima kasih kepada:
- **RedDoorz** untuk business case dan dataset
- **Streamlit Community** untuk tools dan resources

---

<div align="center">

**Dashboard ini dibuat oleh Tim Safari Data 🐱**

*Transforming Data into Actionable Business Insights*

---

© 2025 Tim Safari Data | Proyek Akhir Visualisasi Data

</div>
