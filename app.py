import streamlit as st
import os
import joblib
import numpy as np

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("css/style.css")

# Page Configuration
st.set_page_config(
    page_title="Maternal & Fetal Health Prediction",
    page_icon="🏥",
    layout="wide"
)
# Load Maternal Model
maternal_model = joblib.load("models/maternal_model.pkl")
maternal_encoder = joblib.load("models/maternal_label_encoder.pkl")

# Load Fetal Model
fetal_model = joblib.load("models/fetal_model.pkl")

# Sidebar
st.sidebar.image("images/Health Care Logo.png", width=100)
st.sidebar.title("🏥 Maternal & Fetal Health")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Maternal Health Prediction", "Fetal Health Prediction"]
)

# Home Page
# Home Page
if page == "Home":
    st.title("🏥 Maternal & Fetal Health Prediction System")
    st.image("images/home_banner.png", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h2 style='text-align:center; color:#C2185B;'>
    🤖 AI Powered Maternal & Fetal Healthcare System
    </h2>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
This application uses **Machine Learning** to predict:
- 👩 **Maternal Health Risk**
- 👶 **Fetal Health Status**
It helps healthcare professionals and expectant mothers assess potential risks based on medical parameters.
""")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    <div style="background-color:#FCE4EC; padding:20px; border-radius:15px;">
    <h3 style="color:#C2185B;">👩 Maternal Health Model</h3>
    <p style="color:#333333;"><b>Algorithm:</b> Decision Tree</p>
    <p style="color:#333333;"><b>Accuracy:</b> 81.77%</p>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div style="background-color:#E3F2FD; padding:20px; border-radius:15px;">
    <h3 style="color:#1565C0;">👶 Fetal Health Model</h3>
    <p style="color:#333333;"><b>Algorithm:</b> Random Forest</p>
    <p style="color:#333333;"><b>Accuracy:</b> 94.60%</p>
    </div>
    """, unsafe_allow_html=True)

# Maternal Page
elif page == "Maternal Health Prediction":
    st.title("👩 Maternal Health Risk Prediction")
    st.image("images/mother.png", width=100)
    age = st.number_input("Age", min_value=10, max_value=60, value=25)
    systolic = st.number_input("Systolic Blood Pressure", min_value=50, max_value=250, value=120)
    diastolic = st.number_input("Diastolic Blood Pressure", min_value=30, max_value=150, value=80)
    bs = st.number_input("Blood Sugar (BS)", min_value=0.0, max_value=30.0, value=7.0)
    body_temp = st.number_input("Body Temperature (°F)", min_value=90.0, max_value=110.0, value=98.0)
    heart_rate = st.number_input("Heart Rate", min_value=40, max_value=200, value=80)
    if st.button("Predict Maternal Risk"):
        input_data = np.array([[age, systolic, diastolic, bs, body_temp, heart_rate]])
        prediction = maternal_model.predict(input_data)
        prediction_label = maternal_encoder.inverse_transform(prediction)
        st.success(f"Predicted Risk Level: **{prediction_label[0]}**")

# Fetal Page
elif page == "Fetal Health Prediction":
    st.title("👶 Fetal Health Prediction")
    st.image("images/fetus.png", width=100)
    st.subheader("Enter Fetal Health Parameters")
    col1, col2 = st.columns(2)
    with col1:
        baseline = st.number_input("Baseline Value", value=120.0)
        accelerations = st.number_input("Accelerations", value=0.0)
        fetal_movement = st.number_input("Fetal Movement", value=0.0)
        uterine = st.number_input("Uterine Contractions", value=0.0)
        light = st.number_input("Light Decelerations", value=0.0)
        severe = st.number_input("Severe Decelerations", value=0.0)
        prolongued = st.number_input("Prolongued Decelerations", value=0.0)
        abnormal_short = st.number_input("Abnormal Short Term Variability", value=70.0)
        mean_short = st.number_input("Mean Short Term Variability", value=0.5)
        abnormal_long = st.number_input("Abnormal Long Term Variability", value=40.0)

    with col2:
        mean_long = st.number_input("Mean Long Term Variability", value=8.0)
        histogram_width = st.number_input("Histogram Width", value=60.0)
        histogram_min = st.number_input("Histogram Min", value=50.0)
        histogram_max = st.number_input("Histogram Max", value=180.0)
        histogram_peaks = st.number_input("Histogram Number of Peaks", value=5.0)
        histogram_zeroes = st.number_input("Histogram Number of Zeroes", value=0.0)
        histogram_mode = st.number_input("Histogram Mode", value=120.0)
        histogram_mean = st.number_input("Histogram Mean", value=130.0)
        histogram_median = st.number_input("Histogram Median", value=120.0)
        histogram_variance = st.number_input("Histogram Variance", value=20.0)
        histogram_tendency = st.number_input("Histogram Tendency", value=1.0)

    if st.button("Predict Fetal Health"):

        input_data = np.array([[
            baseline,
            accelerations,
            fetal_movement,
            uterine,
            light,
            severe,
            prolongued,
            abnormal_short,
            mean_short,
            abnormal_long,
            mean_long,
            histogram_width,
            histogram_min,
            histogram_max,
            histogram_peaks,
            histogram_zeroes,
            histogram_mode,
            histogram_mean,
            histogram_median,
            histogram_variance,
            histogram_tendency
        ]])

        prediction = fetal_model.predict(input_data)

        if prediction[0] == 1:
            result = "Normal"

        elif prediction[0] == 2:
            result = "Suspect"

        else:
            result = "Pathological"

        st.success(f"Predicted Fetal Health: **{result}**")