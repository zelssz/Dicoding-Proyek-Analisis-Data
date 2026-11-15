import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="E-Commerce Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Styling CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #444444;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        color: #111111;
        text-align: left;
    }
    .metric-title {
        font-size: 14px;
        color: #555555;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 26px;
        color: #111111;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

sns.set_theme(style="whitegrid")

# -------------------------------------------------------------
# 1. LOAD DATA DARI MAIN_DATA.CSV (Sesuai Kriteria Dicoding)
# -------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

main_df_raw = load_data()

# Mendefinisikan kembali variabel agar kodingan grafik di bawah tetap jalan normal tanpa error
customers_df = main_df_raw[['customer_id', 'customer_unique_id']].drop_duplicates()
orders_df = main_df_raw[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp']].drop_duplicates()
order_items_df = main_df_raw[['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value']]
products_df = main_df_raw[['product_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght', 'product_photos_qty']].drop_duplicates()
category_df = main_df_raw[['product_category_name', 'product_category_name_english']].drop_duplicates()

# -------------------------------------------------------------
# 2. SIDEBAR & FILTER TANGGAL 
# -------------------------------------------------------------
with st.sidebar:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        
        st.image("https://img.icons8.com/ios-filled/100/ffffff/combo-chart.png", width=75)
    
    st.markdown("<h3 style='text-align: center;'>E-Commerce Dashboard</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Filter Data**")
    st.markdown("Pilih rentang waktu analisis pesanan:")

min_date = orders_df['order_purchase_timestamp'].min().date()
max_date = orders_df['order_purchase_timestamp'].max().date()

date_input = st.sidebar.date_input(
    label="Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_input) == 2:
    start_date, end_date = date_input
else:
    start_date = min_date
    end_date = max_date

main_df = orders_df[(orders_df['order_purchase_timestamp'].dt.date >= start_date) & 
                    (orders_df['order_purchase_timestamp'].dt.date <= end_date)]

# -------------------------------------------------------------
# 3. HEADER UTAMA
# -------------------------------------------------------------
st.title("E-Commerce Public Data Analysis Dashboard")
st.markdown("Dashboard interaktif untuk memonitor performa penjualan, analisis kategori produk, serta segmentasi pelanggan berbasis RFM.")
st.markdown("---")

# Hitung Metrik Utama berdasarkan main_df yang sudah difilter
total_orders = main_df['order_id'].nunique()
filtered_order_items = pd.merge(order_items_df, main_df[['order_id']], on='order_id', how='inner')
total_revenue = filtered_order_items['price'].sum()
total_customers = pd.merge(main_df, customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='inner')['customer_unique_id'].nunique()

# Tampilkan Kartu Metrik Utama
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Pesanan</div>
            <div class="metric-value">{total_orders:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Pendapatan</div>
            <div class="metric-value">${total_revenue:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Pelanggan Unik</div>
            <div class="metric-value">{total_customers:,}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------------------------------------
# 4. GRAFIK 1: MENJAWAB PERTANYAAN 1 (TREN PENDAPATAN BULANAN)
# -------------------------------------------------------------
st.subheader("1. Analisis Pendapatan Bulanan")
st.markdown("Grafik tren total pendapatan bulanan untuk mengidentifikasi bulan dengan performa penjualan tertinggi.")

main_df['month_year'] = main_df['order_purchase_timestamp'].dt.to_period('M')
monthly_revenue = pd.merge(filtered_order_items, main_df[['order_id', 'month_year']], on='order_id', how='inner')
monthly_revenue_agg = monthly_revenue.groupby('month_year')['price'].sum().reset_index()
monthly_revenue_agg['month_year'] = monthly_revenue_agg['month_year'].astype(str)

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.plot(
    monthly_revenue_agg['month_year'],
    monthly_revenue_agg['price'] / 1e3,
    marker='o',
    linewidth=2,
    color='#1f77b4'
)
ax.set_title("Total Pendapatan Bulanan (dalam Ribuan USD)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Bulan", fontsize=10)
ax.set_ylabel("Pendapatan ($ Ribuan)", fontsize=10)
plt.xticks(rotation=45)
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

st.info("Insight: Pendapatan bulanan menunjukkan fluktuasi dengan puncak performa tertinggi terjadi pada periode tertentu sesuai rentang data yang aktif.")
st.markdown("---")

# Preprocessing data kategori produk
product_item_df = pd.merge(filtered_order_items, products_df, on='product_id', how='inner')
product_item_df = pd.merge(product_item_df, category_df, on='product_category_name', how='inner')

top_categories = product_item_df['product_category_name_english'].value_counts().reset_index()
top_categories.columns = ['category_name', 'total_sold']

top_5 = top_categories.head(5)
bottom_5 = top_categories.tail(5)

# -------------------------------------------------------------
# 5. GRAFIK 2: KATEGORI PRODUK PALING BANYAK DIMINATI
# -------------------------------------------------------------
st.subheader("2. Kategori Produk Paling Banyak Diminati")
st.markdown("Daftar 5 kategori produk dengan jumlah penjualan tertinggi.")

fig, ax = plt.subplots(figsize=(12, 4))
sns.barplot(
    x='total_sold', y='category_name', data=top_5,
    hue='category_name', legend=False, palette='Blues_r', ax=ax
)
ax.set_title("Top 5 Kategori Produk Terlaris", fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel("Jumlah Terjual", fontsize=10)
ax.set_ylabel("Kategori Produk", fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

st.info("Insight: Kategori produk teratas mendominasi sebagian besar transaksi pembelian dari keseluruhan pelanggan.")
st.markdown("---")

# -------------------------------------------------------------
# 6. GRAFIK 3: KATEGORI PRODUK PALING SEDIKIT DIMINATI
# -------------------------------------------------------------
st.subheader("3. Kategori Produk Paling Sedikit Diminati")
st.markdown("Daftar 5 kategori produk dengan jumlah penjualan terendah.")

fig, ax = plt.subplots(figsize=(12, 4))
sns.barplot(
    x='total_sold', y='category_name', data=bottom_5,
    hue='category_name', legend=False, palette='Reds_r', ax=ax
)
ax.set_title("Top 5 Kategori Produk Paling Sedikit Diminati", fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel("Jumlah Terjual", fontsize=10)
ax.set_ylabel("Kategori Produk", fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

st.info("Insight: Kategori produk di bawah memerlukan strategi promosi atau evaluasi inventaris lebih lanjut karena rendahnya minat beli.")
st.markdown("---")

# -------------------------------------------------------------
# 7. GRAFIK 4: ANALISIS RFM PELANGGAN
# -------------------------------------------------------------
st.subheader("4. Analisis Pelanggan Berbasis RFM")
st.markdown("Segmentasi pelanggan berdasarkan parameter Recency, Frequency, dan Monetary.")

orders_customers_df = pd.merge(main_df, customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='inner')

if not orders_customers_df.empty:
    recent_date = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    rfm_df = orders_customers_df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique'
    }).reset_index()

    item_price = pd.merge(filtered_order_items, orders_customers_df[['order_id', 'customer_unique_id']], on='order_id', how='inner')
    order_spend = item_price.groupby('customer_unique_id')['price'].sum().reset_index()

    rfm_df = rfm_df.merge(order_spend, on='customer_unique_id', how='left').fillna(0)
    rfm_df.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

    top_rfm = rfm_df.sort_values(by='monetary', ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(
        x='monetary', y='customer_unique_id', data=top_rfm,
        hue='customer_unique_id', legend=False, palette='Greens_r', ax=ax
    )
    ax.set_title("Top 5 Pelanggan Berdasarkan Total Pengeluaran (Monetary USD)", fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel("Total Pengeluaran ($)", fontsize=10)
    ax.set_ylabel("Customer Unique ID", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Ringkasan Metrik Rata-Rata RFM")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Average Recency</div>
                <div class="metric-value">{rfm_df['recency'].mean():.1f} Hari</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Average Frequency</div>
                <div class="metric-value">{rfm_df['frequency'].mean():.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Average Monetary</div>
                <div class="metric-value">${rfm_df['monetary'].mean():.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Sampel Data RFM Pelanggan")
    
    rfm_display = rfm_df.head(10).copy()
    rfm_display['monetary'] = rfm_display['monetary'].apply(lambda x: f"${x:,.2f}")
    st.dataframe(rfm_display, width='stretch')
    
    st.info("Insight: Pelanggan dengan nilai Monetary tertinggi dapat dijadikan target utama program loyalitas (VIP customer).")
else:
    st.warning("Silakan pilih rentang tanggal yang mencakup data transaksi.")