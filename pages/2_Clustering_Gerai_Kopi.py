
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Gerai Kopi", page_icon="☕", layout="wide")

st.markdown("""
<style>
:root{
    --bg:#0F1220;
    --panel:#1B2036;
    --amber:#F2A65A;
    --paper:#F5F3EE;
    --ink-soft:#B7BBD1;
}
.stApp{
    background: radial-gradient(circle at 100% 0%, rgba(242,166,90,0.12), transparent 40%), var(--bg);
}
[data-testid="stHeader"]{background:transparent;}
html, body, [class*="css"]{font-family:'Sora','Inter',sans-serif; color:var(--paper);}
h1, h2, h3{color:var(--paper) !important;}
h1{border-left:4px solid var(--amber); padding-left:0.7rem;}
[data-testid="stExpander"], [data-testid="stDataFrame"]{
    background:var(--panel);
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.07);
}
div[data-testid="stMetricValue"], .stMarkdown p{color:var(--ink-soft);}
</style>
""", unsafe_allow_html=True)

st.title("Analisis Klaster Lokasi Gerai Kopi dan Deteksi Zona Sepi")

st.markdown("""
Halaman ini menggunakan **K-Means Clustering** untuk mengelompokkan lokasi
gerai kopi berdasarkan kepadatan penduduk, arus lalu lintas, jumlah kompetitor,
dan koordinat lokasi. Klaster dengan skor aktivitas terendah ditandai
sebagai **zona sepi**.
""")

FEATURES = ["x", "y", "population_density", "traffic_flow", "competitor_count"]

# ------------------------------------------------------------------
# 1. Load Data
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/lokasi_gerai_kopi_clean.csv")
    return df

df = load_data()

with st.expander("🔍 Lihat Dataset"):
    st.dataframe(df.head(20))
    st.write(f"Jumlah baris: {df.shape[0]}, Jumlah kolom: {df.shape[1]}")

# ------------------------------------------------------------------
# 2. Pilih jumlah klaster
# ------------------------------------------------------------------
st.header("⚙️ Pengaturan Clustering")
k = st.slider("Jumlah klaster (k)", min_value=2, max_value=8, value=4)

# ------------------------------------------------------------------
# 3. Training K-Means (cached per nilai k)
# ------------------------------------------------------------------
@st.cache_resource
def train_kmeans(df, k):
    X = df[FEATURES].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    result_df = df.copy()
    result_df["cluster"] = labels

    # Hitung skor "aktivitas" tiap klaster:
    # semakin tinggi kepadatan penduduk & traffic, semakin rendah jumlah kompetitor -> makin ramai
    cluster_profile = result_df.groupby("cluster")[
        ["population_density", "traffic_flow", "competitor_count"]
    ].mean()

    # Normalisasi sederhana untuk membentuk activity_score
    norm_density = (cluster_profile["population_density"] - cluster_profile["population_density"].min()) / (
        cluster_profile["population_density"].max() - cluster_profile["population_density"].min() + 1e-9
    )
    norm_traffic = (cluster_profile["traffic_flow"] - cluster_profile["traffic_flow"].min()) / (
        cluster_profile["traffic_flow"].max() - cluster_profile["traffic_flow"].min() + 1e-9
    )
    norm_competitor = (cluster_profile["competitor_count"] - cluster_profile["competitor_count"].min()) / (
        cluster_profile["competitor_count"].max() - cluster_profile["competitor_count"].min() + 1e-9
    )

    cluster_profile["activity_score"] = norm_density + norm_traffic - norm_competitor

    # Klaster dengan activity_score terendah -> zona sepi
    sepi_cluster = cluster_profile["activity_score"].idxmin()

    result_df["zona"] = result_df["cluster"].apply(
        lambda c: "Sepi" if c == sepi_cluster else "Ramai"
    )

    return result_df, scaler, kmeans, cluster_profile, sepi_cluster

result_df, scaler, kmeans, cluster_profile, sepi_cluster = train_kmeans(df, k)

# ------------------------------------------------------------------
# 4. Visualisasi Scatter Plot
# ------------------------------------------------------------------
st.header("🗺️ Visualisasi Hasil Clustering")

fig, ax = plt.subplots(figsize=(8, 6))
colors = plt.cm.tab10(np.linspace(0, 1, k))

for cluster_id in range(k):
    subset = result_df[result_df["cluster"] == cluster_id]
    label = f"Klaster {cluster_id}" + (" (Zona Sepi)" if cluster_id == sepi_cluster else "")
    marker = "x" if cluster_id == sepi_cluster else "o"
    ax.scatter(subset["x"], subset["y"], s=15, color=colors[cluster_id], label=label, marker=marker, alpha=0.6)

ax.set_xlabel("Koordinat X (mis. Longitude)")
ax.set_ylabel("Koordinat Y (mis. Latitude)")
ax.set_title("Persebaran Gerai Kopi Berdasarkan Klaster")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
st.pyplot(fig)

st.subheader("📊 Profil Rata-Rata Tiap Klaster")
st.dataframe(cluster_profile.style.format("{:.2f}").highlight_min(subset=["activity_score"], color="salmon"))

st.info(f"🔴 **Klaster {sepi_cluster}** teridentifikasi sebagai **Zona Sepi** "
        f"(kepadatan penduduk & lalu lintas rendah, kompetitor relatif tinggi).")

# ------------------------------------------------------------------
# 5. Form Input Lokasi Baru
# ------------------------------------------------------------------
st.header("📍 Cek Lokasi Baru")

col1, col2, col3 = st.columns(3)
with col1:
    new_x = st.number_input("Koordinat X", value=float(df["x"].mean()))
    new_y = st.number_input("Koordinat Y", value=float(df["y"].mean()))
with col2:
    new_density = st.number_input("Population Density", value=float(df["population_density"].mean()))
    new_traffic = st.number_input("Traffic Flow", value=float(df["traffic_flow"].mean()))
with col3:
    new_competitor = st.number_input("Competitor Count", min_value=0, max_value=20,
                                      value=int(df["competitor_count"].mean()))

if st.button("Analisis Lokasi", type="primary"):
    new_point = pd.DataFrame([{
        "x": new_x,
        "y": new_y,
        "population_density": new_density,
        "traffic_flow": new_traffic,
        "competitor_count": new_competitor,
    }])[FEATURES]

    new_point_scaled = scaler.transform(new_point)
    predicted_cluster = kmeans.predict(new_point_scaled)[0]
    zona = "Sepi" if predicted_cluster == sepi_cluster else "Ramai"

    if zona == "Sepi":
        st.error(f"📍 Lokasi ini masuk **Klaster {predicted_cluster}** dan tergolong **ZONA SEPI** ⚠️")
    else:
        st.success(f"📍 Lokasi ini masuk **Klaster {predicted_cluster}** dan tergolong **ZONA RAMAI** ✅")
