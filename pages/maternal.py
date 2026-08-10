import streamlit as st
import joblib
import numpy as np

maternal_model = joblib.load("models/maternal_model.pkl")
maternal_encoder = joblib.load("models/maternal_label_encoder.pkl")

st.title("👩 Maternal Health Risk Prediction")

top_col1, top_col2 = st.columns([2, 1])

with top_col1:
        st.markdown("""
### Enter Mother's Health Information

Fill in the medical details below to predict the maternal health risk.
        """)

with top_col2:
        st.image("images/mother.png", width=220)

st.write("")

col1, col2 = st.columns(2)

with col1:
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=60,
            value=25
        )

        systolic = st.number_input(
            "Systolic Blood Pressure",
            min_value=50,
            max_value=250,
            value=120
        )

        diastolic = st.number_input(
            "Diastolic Blood Pressure",
            min_value=30,
            max_value=150,
            value=80
        )

with col2:
        bs = st.number_input(
            "Blood Sugar (BS)",
            min_value=0.0,
            max_value=30.0,
            value=7.0
        )

        body_temp = st.number_input(
            "Body Temperature (°F)",
            min_value=90.0,
            max_value=110.0,
            value=98.0
        )

        heart_rate = st.number_input(
            "Heart Rate",
            min_value=40,
            max_value=200,
            value=80
        )

st.write("")

if st.button("Predict Maternal Risk"):

        input_data = np.array([[
            age,
            systolic,
            diastolic,
            bs,
            body_temp,
            heart_rate
        ]])

        prediction = maternal_model.predict(input_data)

        prediction_label = maternal_encoder.inverse_transform(prediction)

        risk = prediction_label[0]

        if risk.lower() == "low risk":

            st.markdown("""
<div style="
background:#D4EDDA;
padding:20px;
border-radius:15px;
border-left:8px solid green;
color:black;
font-size:22px;
font-weight:bold;">

🟢 Maternal Health Status : LOW RISK

</div>
""", unsafe_allow_html=True)

        elif risk.lower() == "mid risk":

            st.markdown("""
<div style="
background:#FFF3CD;
padding:20px;
border-radius:15px;
border-left:8px solid orange;
color:black;
font-size:22px;
font-weight:bold;">

🟠 Maternal Health Status : MID RISK

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

🔴 Maternal Health Status : HIGH RISK

</div>
""", unsafe_allow_html=True)