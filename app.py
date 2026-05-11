import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Page config for better UI
st.set_page_config(
    page_title="Laptop Price Predictor",
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

# Load model (Ensure 'laptop_price_model.pkl' is in the same folder)
try:
    model = joblib.load('laptop_price_model.pkl')
except FileNotFoundError:
    st.error("Model file 'laptop_price_model.pkl' not found. Please ensure it's in the same directory.")

# Title and description
st.title("Laptop Price Predictor")
st.markdown("**Adjust specifications in the sidebar to get real-time price estimates**")

# Define all possible categories
companies = ['Apple', 'Asus', 'Chuwi', 'Dell', 'Fujitsu', 'Google', 'HP', 'Huawei', 'LG', 'Lenovo', 'MSI', 'Mediacom', 'Microsoft', 'Razer', 'Samsung', 'Toshiba', 'Vero', 'Xiaomi']
type_names = ['Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation']
cpu_companies = ['Intel', 'AMD']
gpu_companies = ['ARM', 'Intel', 'Nvidia']
os_categories = ['Linux', 'Mac', 'Other/No OS', 'Windows']

# --- NEW: Currency Settings ---
st.sidebar.header("Currency Settings")
exchange_rate = st.sidebar.number_input("EUR to PHP Exchange Rate", min_value=1.0, value=61.00, step=0.50)

st.sidebar.header("Display & Hardware")
inches = st.sidebar.slider("Screen Size (Inches)", min_value=10.0, max_value=18.0, step=0.1, value=15.6)

# Real-world resolutions tied together using select_slider
standard_resolutions = [
    "1366 x 768",   # HD
    "1440 x 900",   # Mac
    "1600 x 900",   # HD+
    "1920 x 1080",  # FHD
    "1920 x 1200",  # WUXGA
    "2560 x 1440",  # QHD
    "2560 x 1600",  # Mac Retina
    "2880 x 1800",  # Mac Retina
    "3200 x 1800",  # QHD+
    "3840 x 2160"   # 4K UHD
]
selected_res = st.sidebar.select_slider("Screen Resolution", options=standard_resolutions, value="1920 x 1080")
# Split the string back into integers for the model
x_res = int(selected_res.split(" x ")[0])
y_res = int(selected_res.split(" x ")[1])

is_touchscreen = st.sidebar.checkbox("Touchscreen", value=False)
has_ips = st.sidebar.checkbox("IPS Display", value=True)

st.sidebar.header("Processor & Memory")
cpu_freq = st.sidebar.slider("CPU Frequency (GHz)", min_value=1.0, max_value=4.0, step=0.1, value=2.5)

# RAM moves in steps of 8
ram = st.sidebar.slider("RAM (GB)", min_value=8, max_value=64, step=8, value=8)
cpu_company = st.sidebar.selectbox("CPU Architecture", ['Intel', 'AMD'])

st.sidebar.header("Storage & Weight")

# Storage options locked to exact powers of 2
storage_options = [0, 128, 256, 512, 1024, 2048]
ssd = st.sidebar.select_slider("SSD Storage (GB)", options=storage_options, value=256)
hdd = st.sidebar.select_slider("HDD Storage (GB)", options=storage_options, value=0)

weight = st.sidebar.slider("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1, value=1.8)

st.sidebar.header("Laptop Details")
company = st.sidebar.selectbox("Brand", companies)
type_name = st.sidebar.selectbox("Laptop Type", type_names)
gpu_company = st.sidebar.selectbox("GPU Company", gpu_companies)
os_category = st.sidebar.selectbox("Operating System", os_categories)

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
    'TypeName_Gaming': [1 if type_name == 'Gaming' else 0],
    'TypeName_Netbook': [1 if type_name == 'Netbook' else 0],
    'TypeName_Notebook': [1 if type_name == 'Notebook' else 0],
    'TypeName_Ultrabook': [1 if type_name == 'Ultrabook' else 0],
    'TypeName_Workstation': [1 if type_name == 'Workstation' else 0],
    'CPU_Company_Intel': [1 if cpu_company == 'Intel' else 0],
    'CPU_Company_Samsung': [1 if cpu_company == 'AMD' else 0],
    'GPU_Company_ARM': [1 if gpu_company == 'ARM' else 0],
    'GPU_Company_Intel': [1 if gpu_company == 'Intel' else 0],
    'GPU_Company_Nvidia': [1 if gpu_company == 'Nvidia' else 0],
    'OS_Category_Linux': [1 if os_category == 'Linux' else 0],
    'OS_Category_Mac': [1 if os_category == 'Mac' else 0],
    'OS_Category_Other/No OS': [1 if os_category == 'Other/No OS' else 0],
    'OS_Category_Windows': [1 if os_category == 'Windows' else 0],
})

# Get real-time prediction
try:
    predicted_price = model.predict(input_data)[0]
except NameError:
    predicted_price = 0.00
    st.warning("Prediction unavailable because the model failed to load.")

# --- NEW: Calculate Peso Price ---
predicted_price_php = predicted_price * exchange_rate

# --- NEW: Display results in 4 columns to fit both currencies ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Price (EUR)", value=f"€{predicted_price:,.2f}")

with col2:
    st.metric(label="Price (PHP)", value=f"₱{predicted_price_php:,.2f}")

with col3:
    total_storage = ssd + hdd
    st.metric(label="Total Storage", value=f"{total_storage} GB")

with col4:
    st.metric(label="Screen PPI", value=f"{ppi:.0f}")

# Display detailed specs in tabs
tab1, tab2, tab3 = st.tabs(["Summary", "Detailed Specs", "Comparison"])

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
        st.write(f"Resolution: {x_res} x {y_res}px")
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
    # --- NEW: Show both currencies in the info box ---
    st.info(f"**Estimated Price: €{predicted_price:,.2f} (₱{predicted_price_php:,.2f})**")
    
    # Show price breakdown context
    col1, col2, col3 = st.columns(3)
    with col1:
        price_per_gb_ram = predicted_price / ram if ram > 0 else 0
        st.metric("Price per GB RAM (EUR)", f"€{price_per_gb_ram:,.0f}")
    with col2:
        price_per_storage = predicted_price / (ssd + hdd) if (ssd + hdd) > 0 else 0
        st.metric("Price per GB Storage (EUR)", f"€{price_per_storage:,.2f}")
    with col3:
        price_per_kg = predicted_price / weight if weight > 0 else 0
        st.metric("Price per kg (EUR)", f"€{price_per_kg:,.0f}")

st.divider()
st.caption("Tip: Adjust the specifications in the sidebar to see real-time price updates!")