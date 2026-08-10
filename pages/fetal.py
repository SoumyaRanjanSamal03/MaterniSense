import streamlit as st
import joblib
import numpy as np

fetal_model = joblib.load("models/fetal_model.pkl")

st.title("👶 Fetal Health Prediction")

top_col1, top_col2 = st.columns([2, 1])

with top_col1:
        st.markdown("""
### Enter Fetal Health Parameters

Fill in the fetal health details below to predict the fetal condition.
        """)

with top_col2:
        st.image("images/fetus.png", width=220)

st.write("")

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

st.write("")

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

        if result == "Normal":

            st.markdown("""
<div style="
background:#D4EDDA;
padding:20px;
border-radius:15px;
border-left:8px solid green;
color:black;
font-size:22px;
font-weight:bold;">

🟢 Fetal Health Status : NORMAL

</div>
""", unsafe_allow_html=True)

        elif result == "Suspect":

            st.markdown("""
<div style="
background:#FFF3CD;
padding:20px;
border-radius:15px;
border-left:8px solid orange;
color:black;
font-size:22px;
font-weight:bold;">

🟠 Fetal Health Status : SUSPECT

</div>
""", unsafe_allow_html=True)

        else:

            st.markdown("""
<div style="
background:#F8D7DA;
padding:20px;
border-radius:15px;
border-left:8px solid red;
color:black;
font-size:22px;
font-weight:bold;">

🔴 Fetal Health Status : PATHOLOGICAL

</div>
""", unsafe_allow_html=True)