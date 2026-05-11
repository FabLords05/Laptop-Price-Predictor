import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Page config for better UI
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .price-highlight {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load('laptop_price_model.pkl')

# Title and description
st.title("💻 Laptop Price Predictor")
st.markdown("**Adjust specifications in the sidebar to get real-time price estimates**")

# Define all possible categories
companies = ['Apple', 'Asus', 'Chuwi', 'Dell', 'Fujitsu', 'Google', 'HP', 'Huawei', 'LG', 'Lenovo', 'MSI', 'Mediacom', 'Microsoft', 'Razer', 'Samsung', 'Toshiba', 'Vero', 'Xiaomi']
type_names = ['Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation']
cpu_companies = ['Intel', 'AMD']
gpu_companies = ['ARM', 'Intel', 'Nvidia']
os_categories = ['Linux', 'Mac', 'Other/No OS', 'Windows']

st.sidebar.header("Display & Hardware")
inches = st.sidebar.slider("Screen Size (Inches)", min_value=10.0, max_value=18.0, step=0.1, value=15.6)
x_res = st.sidebar.slider("X Resolution", min_value=1024, max_value=3840, step=256, value=1920)
y_res = st.sidebar.slider("Y Resolution", min_value=768, max_value=2160, step=256, value=1080)
is_touchscreen = st.sidebar.checkbox("Touchscreen", value=False)
has_ips = st.sidebar.checkbox("IPS Display", value=True)

st.sidebar.header("Processor & Memory")
cpu_freq = st.sidebar.slider("CPU Frequency (GHz)", min_value=1.0, max_value=4.0, step=0.1, value=2.5)
ram = st.sidebar.slider("RAM (GB)", min_value=2, max_value=64, step=2, value=8)
cpu_company = st.sidebar.selectbox("CPU Architecture", ['Intel', 'AMD'])

st.sidebar.header("Storage & Weight")
ssd = st.sidebar.slider("SSD Storage (GB)", min_value=0, max_value=2048, step=128, value=256)
hdd = st.sidebar.slider("HDD Storage (GB)", min_value=0, max_value=2048, step=128, value=0)
weight = st.sidebar.slider("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1, value=1.8)

st.sidebar.header("Laptop Details")
company = st.sidebar.selectbox("Brand", ['Apple', 'Asus', 'Chuwi', 'Dell', 'Fujitsu', 'Google', 'HP', 'Huawei', 'LG', 'Lenovo', 'MSI', 'Mediacom', 'Microsoft', 'Razer', 'Samsung', 'Toshiba', 'Vero', 'Xiaomi'])
type_name = st.sidebar.selectbox("Laptop Type", ['Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation'])
gpu_company = st.sidebar.selectbox("GPU Company", ['ARM', 'Intel', 'Nvidia'])
os_category = st.sidebar.selectbox("Operating System", ['Linux', 'Mac', 'Other/No OS', 'Windows'])

# Calculate PPI (simplified)
ppi = ((x_res**2 + y_res**2)**0.5) / inches

# Create input data with ALL 43 features
input_data = pd.DataFrame({
    'Inches': [inches],
    'CPU_Frequency (GHz)': [cpu_freq],
    'RAM (GB)': [ram],
    'Weight (kg)': [weight],
    'X_Resolution': [x_res],
    'Y_Resolution': [y_res],
    'Is_Touchscreen': [1 if is_touchscreen else 0],
    'Has_IPS': [1 if has_ips else 0],
    'PPI': [ppi],
    'SSD_GB': [ssd],
    'HDD_GB': [hdd],
    # Company one-hot encoding
    'Company_Apple': [1 if company == 'Apple' else 0],
    'Company_Asus': [1 if company == 'Asus' else 0],
    'Company_Chuwi': [1 if company == 'Chuwi' else 0],
    'Company_Dell': [1 if company == 'Dell' else 0],
    'Company_Fujitsu': [1 if company == 'Fujitsu' else 0],
    'Company_Google': [1 if company == 'Google' else 0],
    'Company_HP': [1 if company == 'HP' else 0],
    'Company_Huawei': [1 if company == 'Huawei' else 0],
    'Company_LG': [1 if company == 'LG' else 0],
    'Company_Lenovo': [1 if company == 'Lenovo' else 0],
    'Company_MSI': [1 if company == 'MSI' else 0],
    'Company_Mediacom': [1 if company == 'Mediacom' else 0],
    'Company_Microsoft': [1 if company == 'Microsoft' else 0],
    'Company_Razer': [1 if company == 'Razer' else 0],
    'Company_Samsung': [1 if company == 'Samsung' else 0],
    'Company_Toshiba': [1 if company == 'Toshiba' else 0],
    'Company_Vero': [1 if company == 'Vero' else 0],
    'Company_Xiaomi': [1 if company == 'Xiaomi' else 0],
    # TypeName one-hot encoding
    'TypeName_Gaming': [1 if type_name == 'Gaming' else 0],
    'TypeName_Netbook': [1 if type_name == 'Netbook' else 0],
    'TypeName_Notebook': [1 if type_name == 'Notebook' else 0],
    'TypeName_Ultrabook': [1 if type_name == 'Ultrabook' else 0],
    'TypeName_Workstation': [1 if type_name == 'Workstation' else 0],
    # CPU Company one-hot encoding (AMD maps to Samsung for model compatibility)
    'CPU_Company_Intel': [1 if cpu_company == 'Intel' else 0],
    'CPU_Company_Samsung': [1 if cpu_company == 'AMD' else 0],
    # GPU Company one-hot encoding
    'GPU_Company_ARM': [1 if gpu_company == 'ARM' else 0],
    'GPU_Company_Intel': [1 if gpu_company == 'Intel' else 0],
    'GPU_Company_Nvidia': [1 if gpu_company == 'Nvidia' else 0],
    # OS Category one-hot encoding
    'OS_Category_Linux': [1 if os_category == 'Linux' else 0],
    'OS_Category_Mac': [1 if os_category == 'Mac' else 0],
    'OS_Category_Other/No OS': [1 if os_category == 'Other/No OS' else 0],
    'OS_Category_Windows': [1 if os_category == 'Windows' else 0],
})

# Get real-time prediction
predicted_price = model.predict(input_data)[0]

# Display results in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="💰 Estimated Price", value=f"€{predicted_price:,.2f}", delta=None)

with col2:
    total_storage = ssd + hdd
    st.metric(label="💾 Total Storage", value=f"{total_storage} GB", delta=None)

with col3:
    st.metric(label="📺 Screen PPI", value=f"{ppi:.0f}", delta=None)

# Display detailed specs in tabs
tab1, tab2, tab3 = st.tabs(["📋 Summary", "🔧 Detailed Specs", "📊 Comparison"])

with tab1:
    st.subheader("Selected Configuration")
    summary_data = {
        "Specification": [
            "Brand", "Type", "CPU", "RAM", "Storage", "Screen", 
            "GPU", "OS", "Weight", "Display Features"
        ],
        "Value": [
            company, type_name, f"{cpu_company} @ {cpu_freq}GHz", 
            f"{ram} GB", f"{ssd}GB SSD + {hdd}GB HDD",
            f"{inches}\" ({x_res}x{y_res})",
            gpu_company, os_category, f"{weight} kg",
            f"Touchscreen: {is_touchscreen}, IPS: {has_ips}"
        ]
    }
    st.table(summary_data)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Display Specs")
        st.write(f"Screen Size: {inches}\"")
        st.write(f"X Resolution: {x_res}px")
        st.write(f"Y Resolution: {y_res}px")
        st.write(f"Pixel Density: {ppi:.2f}ppi")
        st.write(f"Touchscreen: {'✓' if is_touchscreen else '✗'}")
        st.write(f"IPS Panel: {'✓' if has_ips else '✗'}")
    
    with col2:
        st.subheader("Hardware Specs")
        st.write(f"CPU: {cpu_company} @ {cpu_freq}GHz")
        st.write(f"RAM: {ram}GB")
        st.write(f"SSD: {ssd}GB")
        st.write(f"HDD: {hdd}GB")
        st.write(f"Weight: {weight}kg")
        st.write(f"GPU: {gpu_company}")

with tab3:
    st.subheader("Price Estimate Details")
    st.info(f"**Estimated Price: €{predicted_price:,.2f}**")
    
    # Show price breakdown context
    col1, col2, col3 = st.columns(3)
    with col1:
        price_per_gb_ram = predicted_price / ram if ram > 0 else 0
        st.metric("Price per GB RAM", f"€{price_per_gb_ram:,.0f}")
    with col2:
        price_per_storage = predicted_price / (ssd + hdd) if (ssd + hdd) > 0 else 0
        st.metric("Price per GB Storage", f"€{price_per_storage:,.2f}")
    with col3:
        price_per_kg = predicted_price / weight if weight > 0 else 0
        st.metric("Price per kg", f"€{price_per_kg:,.0f}")

st.divider()
st.caption("💡 Tip: Adjust the specifications in the sidebar to see real-time price updates!")
