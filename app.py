import os
os.system("pip install -r requirements-new.txt")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
try:
    import seaborn as sns
    st.success("✅ Seaborn loaded successfully!")
except ImportError:
    st.error("❌ Seaborn not installed. Please check requirements.txt.")
    raise

try:
    import plotly.express as px
except ImportError:
    import streamlit as st
    st.error("❌ Plotly is not installed. Please fix requirements.txt.")
    raise


st.set_page_config(
    page_title="📊 Smart Data Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def set_background_gradient():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right top, #fbc2eb, #a6c1ee);
            background-attachment: fixed;
        }
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            color: #333333;
        }
        .metric-container {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

set_background_gradient()

st.title("📊 Smart Data Analyzer Dashboard")
st.subheader("Upload your CSV and explore insights visually")
st.markdown("---")

uploaded_file = st.file_uploader("📂 Upload CSV File", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File loaded successfully!")

    st.markdown("### 🧾 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown("---")

    st.markdown("### 📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total Rows", f"{len(df):,}")
    with col2:
        if 'Amount' in df.columns:
            st.metric("💰 Total Amount", f"{df['Amount'].sum():,.0f}")
    with col3:
        if 'Profit' in df.columns:
            st.metric("📈 Total Profit", f"{df['Profit'].sum():,.0f}")
    with col4:
        if 'Quantity' in df.columns:
            st.metric("🔢 Total Quantity", f"{df['Quantity'].sum():,.0f}")

    st.markdown("---")

    st.sidebar.header("🔎 Filter Data")
    for col in df.select_dtypes(include='object').columns:
        unique_vals = df[col].dropna().unique()
        selected_vals = st.sidebar.multiselect(f"Filter {col}:", unique_vals, default=unique_vals)
        df = df[df[col].isin(selected_vals)]

    st.markdown("### 📈 Visualizations")
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    if num_cols and cat_cols:
        col_x = st.selectbox("Choose Category (X-axis)", cat_cols)
        col_y = st.selectbox("Choose Value (Y-axis)", num_cols)

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.plotly_chart(px.bar(df, x=col_x, y=col_y, color=col_x,
                                   title=f"{col_y} by {col_x}"), use_container_width=True)
        with chart_col2:
            st.plotly_chart(px.pie(df, names=col_x, values=col_y, hole=0.4,
                                   title=f"{col_y} Distribution"), use_container_width=True)

    if len(num_cols) >= 2:
        st.markdown("### 🔥 Compact Correlation Heatmap")
        heat_col1, heat_col2, heat_col3 = st.columns([2, 3, 2])
        with heat_col2:
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.heatmap(df[num_cols].corr(), annot=True, cmap="YlGnBu", fmt=".2f", ax=ax, cbar=False)
            st.pyplot(fig)

else:
    st.info("👆 Please upload a `.csv` file to start analyzing.")
