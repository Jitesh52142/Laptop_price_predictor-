import streamlit as st
import pickle
import numpy as np

# ✅ Load models and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# 🌟 Add custom CSS styling
st.markdown("""
    <style>
    /* 🌑 Dark Mode */
    .stApp {
        background: linear-gradient(135deg, #1c1c1c, #2c2c2c);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ✅ Title Styling */
    .title {
        font-size: 56px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 40px;
        text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.5);
    }

    /* ✅ Form Section Styling */
    .st-form {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: #ffffff;
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.7);
        margin-bottom: 40px;
        transition: all 0.3s ease;
    }

    /* ✅ Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 14px 35px;
        font-size: 18px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.3s, background 0.3s;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #3e8e41, #37a844);
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0, 255, 0, 0.6);
    }

    /* ✅ Result Box Styling */
    .result-box {
        background: #2c2c2c;
        color: #4CAF50;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0, 255, 0, 0.7);
        font-size: 26px;
        text-align: center;
        margin-top: 30px;
        transition: all 0.3s ease;
    }

    /* ✅ Alert Box Styling */
    .alert-box {
        background: #ff4d4d;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-size: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 🛠️ App Title
st.markdown('<div class="title">💻 Laptop Price Predictor</div>', unsafe_allow_html=True)

# ✅ Form Section
with st.container():
    col1, col2 = st.columns(2)

    # Column 1: Laptop specs
    with col1:
        company = st.selectbox('🔹 **Brand**', df['Company'].unique(), key='company')
        type = st.selectbox('🔹 **Type**', df['TypeName'].unique(), key='type')
        Ram = st.selectbox('🔹 **RAM (in GB)**', [2, 4, 6, 8, 12, 16, 24, 32, 64], key='ram')
        weight = st.number_input('🔹 **Weight (in kg)**', min_value=0.5, step=0.1, key='weight')

        touchscreen = st.radio('🔹 **Touchscreen**', ['Yes', 'No'], key='touchscreen')
        ips = st.radio('🔹 **IPS Display**', ['Yes', 'No'], key='ips')

    # Column 2: Display and storage
    with col2:
        Screen_size = st.number_input('📏 **Screen Size (in inches)**', min_value=10.0, step=0.1, key='screen_size')
        resolution = st.selectbox('🖥️ **Screen Resolution**', 
                                  ['1920x1080', '1366x768', '1600x900', '3840x2160',
                                   '3200x1800', '2880x1800', '2560x1600', '2560x1440',
                                   '2304x1440'], key='resolution')

        Cpu = st.selectbox('⚙️ **CPU**', df['CPU brand'].unique(), key='cpu')
        Gpu = st.selectbox('🎮 **GPU**', df['Gpu brand'].unique(), key='gpu')
        os = st.selectbox('🛠️ **Operating System**', df['os'].unique(), key='os')

        # HDD/SSD with validation logic
        hdd = st.selectbox('💾 **HDD (in GB)**', [0, 128, 256, 512, 1024, 2048], key='hdd')
        ssd = st.selectbox('🔋 **SSD (in GB)**', [0, 8, 128, 256, 512, 1024], key='ssd')

        # ✅ Auto-fill logic
        if hdd > 0 and ssd == 0:
            ssd = 0
        elif ssd > 0 and hdd == 0:
            hdd = 0

# ✅ Prediction Button
if st.button('🚀 **Predict Price**'):
    # 🔥 Validation: Check for missing fields
    if (
        not company or not type or not Ram or weight <= 0 or 
        not touchscreen or not ips or Screen_size <= 0 or 
        not resolution or not Cpu or not Gpu or not os
    ):
        st.markdown('<div class="alert-box">⚠️ Please fill all the fields before predicting!</div>', unsafe_allow_html=True)

    # 🔥 Validate HDD/SSD logic: One must be filled
    elif hdd == 0 and ssd == 0:
        st.markdown('<div class="alert-box">⚠️ You must fill either HDD or SSD with a valid value!</div>', unsafe_allow_html=True)
    
    else:
        # Converting categorical features
        touchscreen = 1 if touchscreen == 'Yes' else 0
        ips = 1 if ips == 'Yes' else 0

        # Screen resolution processing
        x_res, y_res = map(int, resolution.split('x'))
        ppi = ((x_res**2) + (y_res**2))**0.5 / Screen_size

        # Create query array
        query = np.array([company, type, Ram, weight, touchscreen, ips, ppi, Cpu, hdd, ssd, Gpu, os])
        query = query.reshape(1, 12)

        # ✅ Prediction
        predicted_price = int(np.exp(pipe.predict(query)))

        # 💡 Display result
        st.markdown(f"""
            <div class="result-box">
                💰 The predicted price of this configuration is:  
                <strong>₹ {predicted_price}</strong>
            </div>
        """, unsafe_allow_html=True)
