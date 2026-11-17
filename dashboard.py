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

# Styling CSS untuk Kartu Metrik Utama
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
# 1. LOAD DATA DARI MAIN_DATA.CSV
# -------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

main_df_raw = load_data()

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
# 3. HEADER UTAMA & METRIK KARTU ATAS
# -------------------------------------------------------------
st.title("E-Commerce Public Data Analysis Dashboard")
st.markdown("Dashboard interaktif untuk memonitor performa penjualan, analisis kategori produk, serta segmentasi pelanggan berbasis RFM.")
st.markdown("---")

total_orders = main_df['order_id'].nunique()
filtered_order_items = pd.merge(order_items_df, main_df[['order_id']], on='order_id', how='inner')
total_revenue = filtered_order_items['price'].sum()
total_customers = pd.merge(main_df, customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='inner')['customer_unique_id'].nunique()

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
            <div class="metric-value">R$ {total_revenue:,.2f}</div>
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
# 4. GRAFIK 1: TREN PENDAPATAN BULANAN (Jan - Ags 2018)
# -------------------------------------------------------------
st.subheader("1. Tren Pendapatan Bulanan (Januari - Agustus 2018)")

# Mengambil data orders langsung untuk rentang Jan-Ags 2018 secara independen
orders_q1_raw = orders_df[
    (orders_df['order_purchase_timestamp'] >= '2018-01-01') & 
    (orders_df['order_purchase_timestamp'] <= '2018-08-31')
].copy()

orders_q1_raw['order_month'] = orders_q1_raw['order_purchase_timestamp'].dt.strftime('%Y-%m')

# Gabungkan dengan order_items untuk menghitung total revenue (harga barang + freight atau price saja sesuai Colab)
rev_q1_items = pd.merge(order_items_df, orders_q1_raw[['order_id', 'order_month']], on='order_id', how='inner')
monthly_revenue_q1 = rev_q1_items.groupby('order_month')['price'].sum().reset_index()
monthly_revenue_q1.rename(columns={'price': 'total_revenue'}, inplace=True)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    monthly_revenue_q1['order_month'],
    monthly_revenue_q1['total_revenue'],
    marker='o',
    linewidth=2,
    color='#72BCD4'
)
ax.set_title("Tren Pendapatan Bulanan (Januari 2018 - Agustus 2018)", loc="center", fontsize=14, fontweight='bold')
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Pendapatan (BRL)", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
st.pyplot(fig)
st.markdown("---")

# -------------------------------------------------------------
# 5. GRAFIK 2: PERFORMA KATEGORI PRODUK TERBAIK & TERBURUK (Subplot)
# -------------------------------------------------------------
st.subheader("2. Kategori Produk dengan Penjualan Tertinggi dan Terendah")

# Menggunakan data dari rentang waktu yang sama seperti di Colab (Sep 2016 - Ags 2018)
df_q2 = main_df[
    (main_df['order_purchase_timestamp'] >= '2016-09-01') & 
    (main_df['order_purchase_timestamp'] <= '2018-08-31')
].copy()

q2_items = pd.merge(order_items_df, df_q2[['order_id']], on='order_id', how='inner')
q2_prod = pd.merge(q2_items, products_df, on='product_id', how='inner')
q2_cat = pd.merge(q2_prod, category_df, on='product_category_name', how='inner')

category_sales = q2_cat.groupby(by="product_category_name_english").order_item_id.sum().reset_index()
category_sales.rename(columns={"order_item_id": "total_items_sold"}, inplace=True)

top_products = category_sales.sort_values(by='total_items_sold', ascending=False).head(5)
bottom_products = category_sales.sort_values(by='total_items_sold', ascending=True).head(5)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Grafik Kiri: Top 5 Kategori Terbaik
sns.barplot(x="total_items_sold", y="product_category_name_english", data=top_products, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Unit Terjual", fontsize=12)
ax[0].set_title("Top 5 Kategori Produk dengan Penjualan Tertinggi", loc="center", fontsize=14, fontweight='bold')
ax[0].tick_params(axis='y', labelsize=11)

# Grafik Kanan: Top 5 Kategori Terburuk
sns.barplot(x="total_items_sold", y="product_category_name_english", data=bottom_products, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Unit Terjual", fontsize=12)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Top 5 Kategori Produk dengan Penjualan Terendah", loc="center", fontsize=14, fontweight='bold')
ax[1].tick_params(axis='y', labelsize=11)

plt.suptitle("Performa Kategori Produk Berdasarkan Jumlah Penjualan (Sep 2016 - Ags 2018)", fontsize=18, fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
st.markdown("---")

# -------------------------------------------------------------
# 6. GRAFIK 3: ANALISIS RFM PELANGGAN (Top 5 Monetary BRL)
# -------------------------------------------------------------
st.subheader("3. Analisis Pelanggan Berbasis RFM (Top Monetary)")

orders_customers_df = pd.merge(main_df, customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='inner')

if not orders_customers_df.empty:
    recent_date = orders_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    rfm_df = orders_customers_df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique'
    }).reset_index()

    item_price = pd.merge(filtered_order_items, orders_customers_df[['order_id', 'customer_unique_id']], on='order_id', how='inner')
    order_spend = item_price.groupby('customer_unique_id')['price'].sum().reset_index()

    rfm_df = rfm_df.merge(order_spend, on='customer_unique_id', how='left').fillna(0)
    rfm_df.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

    top_5_monetary = rfm_df.sort_values(by='monetary', ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x='monetary',
        y='customer_unique_id',
        data=top_5_monetary,
        hue='customer_unique_id',
        legend=False,
        palette='Greens_r',
        ax=ax
    )
    ax.set_title("Top 5 Pelanggan Berdasarkan Total Pengeluaran (Monetary BRL)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Total Pengeluaran (BRL)", fontsize=12)
    ax.set_ylabel("Customer Unique ID", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
