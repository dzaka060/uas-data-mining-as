try:
    import streamlit as st  # type: ignore[import]
except Exception:
    # Fallback stub for environments where streamlit is not installed (e.g., linting)
    class _DummyColumn:
        def __enter__(self):
            return None
        def __exit__(self, exc_type, exc, tb):
            return False

    class _DummySt:
        def set_page_config(self, *a, **k):
            return None
        def title(self, *a, **k):
            return None
        def markdown(self, *a, **k):
            return None
        def expander(self, *a, **k):
            class _Ctx:
                def __enter__(self):
                    return None
                def __exit__(self, exc_type, exc, tb):
                    return False
            return _Ctx()
        def dataframe(self, *a, **k):
            return None
        def write(self, *a, **k):
            return None
        def header(self, *a, **k):
            return None
        def selectbox(self, *a, **k):
            # return first option if provided, else None
            options = a[1] if len(a) > 1 else k.get('options')
            if options:
                try:
                    return list(options)[0]
                except Exception:
                    return None
            return None
        def columns(self, n):
            return tuple(_DummyColumn() for _ in range(n))
        def number_input(self, *a, **k):
            return k.get('value', 0)
        def button(self, *a, **k):
            return False
        def error(self, *a, **k):
            return None
        def success(self, *a, **k):
            return None
        def pyplot(self, *a, **k):
            return None
        # decorators: act as identity when streamlit not available
        def cache_data(self, func=None, **kw):
            if func:
                return func
            def _dec(f):
                return f
            return _dec
        def cache_resource(self, func=None, **kw):
            if func:
                return func
            def _dec(f):
                return f
            return _dec

    st = _DummySt()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

st.set_page_config(page_title="Prediksi Diabetes", page_icon="🩺", layout="wide")

st.markdown("""
<style>
:root{
    --bg:#0F1220;
    --panel:#1B2036;
    --cyan:#4CD6C0;
    --paper:#F5F3EE;
    --ink-soft:#B7BBD1;
}
.stApp{
    background: radial-gradient(circle at 100% 0%, rgba(76,214,192,0.12), transparent 40%), var(--bg);
}
[data-testid="stHeader"]{background:transparent;}
html, body, [class*="css"]{font-family:'Sora','Inter',sans-serif; color:var(--paper);}
h1, h2, h3{color:var(--paper) !important;}
h1{border-left:4px solid var(--cyan); padding-left:0.7rem;}
[data-testid="stExpander"], [data-testid="stDataFrame"]{
    background:var(--panel);
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.07);
}
div[data-testid="stMetricValue"], .stMarkdown p{color:var(--ink-soft);}
</style>
""", unsafe_allow_html=True)

st.title("🩺 Prediksi Risiko Diabetes Berdasarkan Data Pasien")

st.markdown("""
Halaman ini membangun tiga model klasifikasi (**KNN**, **Naive Bayes**, dan
**Decision Tree**) untuk memprediksi apakah seorang pasien berisiko
mengidap diabetes, menggunakan dataset **Pima Indians Diabetes**.
""")

# ------------------------------------------------------------------
# 1. Load & Preprocess Data
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/diabetes.csv")
    # Kolom yang secara medis tidak mungkin bernilai 0 -> anggap sebagai missing value
    cols_with_invalid_zero = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    for col in cols_with_invalid_zero:
        df[col] = df[col].replace(0, np.nan)
        df[col] = df[col].fillna(df[col].median())
    return df

df = load_data()

with st.expander("🔍 Lihat Dataset"):
    st.dataframe(df.head(20))
    st.write(f"Jumlah baris: {df.shape[0]}, Jumlah kolom: {df.shape[1]}")

# ------------------------------------------------------------------
# 2. Train Models (cached so training only runs once)
# ------------------------------------------------------------------
@st.cache_resource
def train_models(df):
    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5),
    }

    results = {}
    for name, model in models.items():
        # KNN sensitif terhadap skala, jadi pakai data yang sudah di-scale
        if name == "KNN":
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        results[name] = {
            "model": model,
            "y_test": y_test,
            "y_pred": y_pred,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
        }

    return results, scaler, X.columns.tolist()

results, scaler, feature_names = train_models(df)

# ------------------------------------------------------------------
# 3. Metrik Evaluasi
# ------------------------------------------------------------------
st.header("📈 Metrik Evaluasi Model")

metric_df = pd.DataFrame({
    name: {
        "Akurasi": res["accuracy"],
        "Precision": res["precision"],
        "Recall": res["recall"],
        "F1-Score": res["f1"],
    }
    for name, res in results.items()
}).T

st.dataframe(metric_df.style.format("{:.3f}").highlight_max(axis=0, color="lightgreen"))

# ------------------------------------------------------------------
# 4. Confusion Matrix
# ------------------------------------------------------------------
st.header("🧮 Confusion Matrix")

selected_model_cm = st.selectbox(
    "Pilih model untuk melihat Confusion Matrix:",
    list(results.keys()),
    key="cm_select"
)

cm = confusion_matrix(results[selected_model_cm]["y_test"], results[selected_model_cm]["y_pred"])

fig, ax = plt.subplots(figsize=(4, 3))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Tidak Diabetes", "Diabetes"],
            yticklabels=["Tidak Diabetes", "Diabetes"], ax=ax)
ax.set_xlabel("Prediksi")
ax.set_ylabel("Aktual")
ax.set_title(f"Confusion Matrix - {selected_model_cm}")
st.pyplot(fig)

# ------------------------------------------------------------------
# 5. Form Prediksi
# ------------------------------------------------------------------
st.header("🔮 Coba Prediksi Pasien Baru")

selected_model_pred = st.selectbox(
    "Pilih model untuk prediksi:",
    list(results.keys()),
    key="pred_select"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
    glucose = st.number_input("Glucose", min_value=0, max_value=300, value=120)
with col2:
    blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=70)
    skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)
with col3:
    insulin = st.number_input("Insulin", min_value=0, max_value=900, value=80)
    bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0)
with col4:
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5)
    age = st.number_input("Age", min_value=1, max_value=120, value=30)

if st.button("Prediksi Sekarang", type="primary"):
    input_data = pd.DataFrame([{
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age,
    }])[feature_names]

    model = results[selected_model_pred]["model"]

    if selected_model_pred == "KNN":
        input_scaled = scaler.transform(input_data)
        pred = model.predict(input_scaled)[0]
        proba = model.predict_proba(input_scaled)[0][1]
    else:
        pred = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0][1]

    if pred == 1:
        st.error(f"⚠️ Pasien **diprediksi DIABETES** (probabilitas: {proba:.1%})")
    else:
        st.success(f"✅ Pasien **diprediksi TIDAK diabetes** (probabilitas diabetes: {proba:.1%})")
