import streamlit as st
import joblib
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# -----------------------------
# Load CSS
# -----------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MaterniSense",
    page_icon="🏥",
    layout="wide"
)

local_css("css/style.css")

# -----------------------------
# Load Models
# -----------------------------
maternal_model = joblib.load("models/maternal_model.pkl")
maternal_encoder = joblib.load("models/maternal_label_encoder.pkl")

fetal_model = joblib.load("models/fetal_model.pkl")

def generate_pdf(filename, title, details):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>MaterniSense</b>", styles['Title']))
    story.append(Paragraph(title, styles['Heading2']))
    story.append(Paragraph("<br/>", styles['Normal']))

    for item in details:
        story.append(Paragraph(item, styles['BodyText']))

    story.append(Paragraph("<br/>", styles['Normal']))
    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles['Italic']
        )
    )

    doc.build(story)

# ===========================
# Prediction History
# ===========================

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image("images/Health Care Logo.png", width=100)

st.sidebar.title("🏥 MaterniSense")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go To",
    [
        "Home",
        "Maternal Health Prediction",
        "Fetal Health Prediction",
        "About Project"
    ]
)

# ======================================================
# HOME PAGE
# ======================================================

if page == "Home":

    st.title("🏥 MaterniSense")

    st.image("images/home_banner.png", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="text-align:center;color:#C2185B;">
    🤖 AI Powered Maternal & Fetal Healthcare System
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    text-align:center;
    font-size:18px;
    color:#333333;">

    Welcome to <b>MaterniSense</b>.

    An AI-powered healthcare application that predicts
    <b>Maternal Health Risk</b> and
    <b>Fetal Health Status</b> using Machine Learning.

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### 👩 Maternal Health Model

**Algorithm:** Decision Tree

**Accuracy:** **81.77%**
""")

    with col2:

        st.success("""
### 👶 Fetal Health Model

**Algorithm:** Random Forest

**Accuracy:** **94.60%**
""")

    st.write("")

    st.markdown("""
---
### 🌟 Key Features

✅ Maternal Health Risk Prediction

✅ Fetal Health Status Prediction

✅ Prediction Confidence Score

✅ Patient Summary

✅ Health Recommendations

✅ PDF Report Download

✅ Prediction History
""")

    # ===========================
    # Prediction History
    # ===========================

    st.write("")
    st.subheader("📜 Prediction History")

    if len(st.session_state.history) > 0:

        history_df = pd.DataFrame(st.session_state.history)

        st.dataframe(history_df, use_container_width=True)

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download History (CSV)",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv"
        )

        if st.button("🗑 Clear History"):

            st.session_state.history = []

            st.rerun()

    else:

        st.info("No predictions have been made yet.")
# ============================
# Maternal Health Prediction Page
# ============================

elif page == "Maternal Health Prediction":

    st.title("👩 Maternal Health Risk Prediction")

    # ---------------- Header ----------------

    top_col1, top_col2 = st.columns([2, 1])

    with top_col1:

        st.markdown("""
### Enter Mother's Health Information

Fill in the medical details below to predict the maternal health risk.
""")

    with top_col2:

        st.image("images/mother.png", width=220)

    st.write("")

    # ---------------- Input Fields ----------------

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

    # ---------------- Prediction ----------------

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

        # ---------------- Confidence ----------------

        if hasattr(maternal_model, "predict_proba"):

            probabilities = maternal_model.predict_proba(input_data)

            confidence = np.max(probabilities) * 100

        else:

            confidence = None

        prediction_label = maternal_encoder.inverse_transform(prediction)

        risk = prediction_label[0]

        # ---------------- Patient Summary ----------------

        st.subheader("📋 Patient Summary")

        st.markdown(f"""
<div style="
background-color:#F8F9FA;
padding:20px;
border-radius:15px;
border:2px solid #0D6EFD;
color:black;
font-size:18px;">

<b>👤 Age:</b> {age} Years<br><br>
<b>🩸 Blood Pressure:</b> {systolic}/{diastolic} mmHg<br><br>
<b>🧪 Blood Sugar:</b> {bs} mmol/L<br><br>
<b>🌡 Body Temperature:</b> {body_temp} °F<br><br>
<b>❤️ Heart Rate:</b> {heart_rate} bpm

</div>
""", unsafe_allow_html=True)

        st.write("")

               # ---------------- Prediction Result ----------------

        if risk.lower() == "low risk":

            st.markdown("""
            <div style="
                background-color:#D4EDDA;
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
                background-color:#FFF3CD;
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
                background-color:#F8D7DA;
                padding:20px;
                border-radius:15px;
                border-left:8px solid red;
                color:black;
                font-size:22px;
                font-weight:bold;">

                🔴 Maternal Health Status : HIGH RISK

            </div>
            """, unsafe_allow_html=True)

        # ---------------- Prediction Confidence ----------------

        if confidence is not None:

            st.write("")
            st.subheader("📊 Prediction Confidence")

            st.progress(confidence / 100)

            st.success(f"Model Confidence: {confidence:.2f}%")

        # ---------------- Health Recommendations ----------------

        st.write("")
        st.subheader("🩺 Health Recommendations")

        if risk.lower() == "low risk":

            st.success("""
✅ Continue regular prenatal check-ups.
✅ Eat a balanced and nutritious diet.
✅ Stay hydrated.
✅ Exercise regularly as advised by your doctor.
✅ Get adequate rest and sleep.
""")

        elif risk.lower() == "mid risk":

            st.warning("""
⚠ Monitor blood pressure regularly.
⚠ Visit your doctor more frequently.
⚠ Reduce stress and avoid heavy work.
⚠ Follow prescribed medications.
⚠ Maintain a healthy lifestyle.
""")

        else:

            st.error("""
🚨 Seek immediate medical attention.
🚨 Attend all prenatal check-ups.
🚨 Monitor blood pressure and blood sugar regularly.
🚨 Follow your doctor's advice strictly.
🚨 Avoid self-medication.
""")

        # ---------------- Prediction History ----------------

        st.session_state.history.append({

          "Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

          "Prediction Type": "Maternal",

          "Result": risk,

          "Confidence": f"{confidence:.2f}%" if confidence is not None else "N/A"

})

# ---------------- PDF Report ----------------

        details = [

            "<b>Patient Summary</b>",
            f"Age : {age} Years",
            f"Blood Pressure : {systolic}/{diastolic} mmHg",
            f"Blood Sugar : {bs} mmol/L",
            f"Body Temperature : {body_temp} °F",
            f"Heart Rate : {heart_rate} bpm",
            "<br/>",
            f"<b>Prediction Result :</b> {risk}",

        ]

        if confidence is not None:
            details.append(f"<b>Confidence :</b> {confidence:.2f}%")

        details.append("<br/><b>Health Recommendations</b>")

        if risk.lower() == "low risk":

            details.extend([
                "Continue regular prenatal check-ups.",
                "Eat a balanced and nutritious diet.",
                "Stay hydrated.",
                "Exercise regularly as advised by your doctor.",
                "Get adequate rest and sleep."
            ])

        elif risk.lower() == "mid risk":

            details.extend([
                "Monitor blood pressure regularly.",
                "Visit your doctor more frequently.",
                "Reduce stress and avoid heavy work.",
                "Follow prescribed medications.",
                "Maintain a healthy lifestyle."
             ])

        else:

            details.extend([
                "Seek immediate medical attention.",
                "Attend all prenatal check-ups.",
                "Monitor blood pressure and blood sugar regularly.",
                "Follow your doctor's advice strictly.",
                "Avoid self-medication."
            ])

        generate_pdf(
            "maternal_report.pdf",
            "Maternal Health Prediction Report",
            details
        )

        with open("maternal_report.pdf", "rb") as pdf_file:

            st.download_button(
                label="📄 Download Prediction Report",
                data=pdf_file,
                file_name="Maternal_Health_Report.pdf",
                mime="application/pdf"
            )
            
            
# ============================
# Fetal Health Prediction Page
# ============================

elif page == "Fetal Health Prediction":

    st.title("👶 Fetal Health Prediction")

    # ---------------- Header ----------------

    top_col1, top_col2 = st.columns([2, 1])

    with top_col1:
        st.markdown("""
### Enter Fetal Health Parameters

Fill in the fetal health details below to predict the fetal condition.
""")

    with top_col2:
        st.image("images/fetus.png", width=220)

    st.write("")

    # ---------------- Input Section ----------------

    col1, col2 = st.columns(2)

    with col1:

        baseline = st.number_input("Baseline Value", value=120.0)
        accelerations = st.number_input("Accelerations", value=0.0)
        fetal_movement = st.number_input("Fetal Movement", value=0.0)
        uterine = st.number_input("Uterine Contractions", value=0.0)
        light = st.number_input("Light Decelerations", value=0.0)
        severe = st.number_input("Severe Decelerations", value=0.0)
        prolongued = st.number_input("Prolongued Decelerations", value=0.0)
        abnormal_short = st.number_input(
            "Abnormal Short Term Variability",
            value=70.0
        )

        mean_short = st.number_input(
            "Mean Short Term Variability",
            value=0.5
        )

        abnormal_long = st.number_input(
            "Abnormal Long Term Variability",
            value=40.0
        )

    with col2:

        mean_long = st.number_input(
            "Mean Long Term Variability",
            value=8.0
        )

        histogram_width = st.number_input(
            "Histogram Width",
            value=60.0
        )

        histogram_min = st.number_input(
            "Histogram Min",
            value=50.0
        )

        histogram_max = st.number_input(
            "Histogram Max",
            value=180.0
        )

        histogram_peaks = st.number_input(
            "Histogram Number of Peaks",
            value=5.0
        )

        histogram_zeroes = st.number_input(
            "Histogram Number of Zeroes",
            value=0.0
        )

        histogram_mode = st.number_input(
            "Histogram Mode",
            value=120.0
        )

        histogram_mean = st.number_input(
            "Histogram Mean",
            value=130.0
        )

        histogram_median = st.number_input(
            "Histogram Median",
            value=120.0
        )

        histogram_variance = st.number_input(
            "Histogram Variance",
            value=20.0
        )

        histogram_tendency = st.number_input(
            "Histogram Tendency",
            value=1.0
        )

    st.write("")

    # ---------------- Prediction ----------------

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

        if hasattr(fetal_model, "predict_proba"):
            probabilities = fetal_model.predict_proba(input_data)
            confidence = np.max(probabilities) * 100
        else:
            confidence = None

        # ---------------- Fetal Parameters Summary ----------------

        st.subheader("📋 Fetal Parameters Summary")

        st.markdown(f"""
        <div style="
            background-color:#F8F9FA;
            padding:20px;
            border-radius:15px;
            border:2px solid #0D6EFD;
            color:black;
            font-size:18px;">

        <b>❤️ Baseline Value:</b> {baseline}<br><br>
        <b>📈 Accelerations:</b> {accelerations}<br><br>
        <b>👶 Fetal Movement:</b> {fetal_movement}<br><br>
        <b>🤰 Uterine Contractions:</b> {uterine}<br><br>
        <b>🌡 Mean Long Term Variability:</b> {mean_long}<br><br>
        <b>📊 Histogram Mean:</b> {histogram_mean}

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ---------------- Prediction Result ----------------

        if prediction[0] == 1:
            result = "Normal"

            st.markdown("""
            <div style="
                background-color:#D4EDDA;
                padding:20px;
                border-radius:15px;
                border-left:8px solid green;
                color:black;
                font-size:22px;
                font-weight:bold;">

                🟢 Fetal Health Status : NORMAL

            </div>
            """, unsafe_allow_html=True)

        elif prediction[0] == 2:
            result = "Suspect"

            st.markdown("""
            <div style="
                background-color:#FFF3CD;
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
            result = "Pathological"

            st.markdown("""
            <div style="
                background-color:#F8D7DA;
                padding:20px;
                border-radius:15px;
                border-left:8px solid red;
                color:black;
                font-size:22px;
                font-weight:bold;">

                🔴 Fetal Health Status : PATHOLOGICAL

            </div>
            """, unsafe_allow_html=True)

        # ---------------- Prediction Confidence ----------------

        if confidence is not None:

            st.write("")
            st.subheader("📊 Prediction Confidence")

            st.progress(confidence / 100)

            st.success(f"Model Confidence: {confidence:.2f}%")

        # ---------------- Health Recommendations ----------------

        st.write("")
        st.subheader("🩺 Health Recommendations")

        if result == "Normal":

            st.success("""
✅ Continue regular prenatal check-ups.
✅ Maintain a healthy and balanced diet.
✅ Stay hydrated.
✅ Continue routine fetal monitoring.
✅ Follow your doctor's advice.
""")

        elif result == "Suspect":

            st.warning("""
⚠ Schedule additional prenatal check-ups.
⚠ Monitor fetal movements regularly.
⚠ Follow your doctor's recommendations.
⚠ Maintain a healthy lifestyle.
⚠ Report any unusual symptoms immediately.
""")

        else:

            st.error("""
🚨 Seek immediate medical attention.
🚨 Continuous fetal monitoring is recommended.
🚨 Attend all prenatal appointments.
🚨 Follow your doctor's instructions strictly.
🚨 Do not delay treatment if symptoms worsen.
""")

                    # ---------------- Prediction History ----------------

        st.session_state.history.append({

            "Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

            "Prediction Type": "Fetal",

            "Result": result,

            "Confidence": f"{confidence:.2f}%" if confidence is not None else "N/A"

        })

                   # ---------------- PDF Report ----------------

        details = [

            "<b>Fetal Parameters Summary</b>",
            f"Baseline Value : {baseline}",
            f"Accelerations : {accelerations}",
            f"Fetal Movement : {fetal_movement}",
            f"Uterine Contractions : {uterine}",
            f"Mean Long Term Variability : {mean_long}",
            f"Histogram Mean : {histogram_mean}",
            "<br/>",
            f"<b>Prediction Result :</b> {result}",

        ]

        if confidence is not None:
            details.append(f"<b>Confidence :</b> {confidence:.2f}%")

        details.append("<br/><b>Health Recommendations</b>")

        if result == "Normal":

            details.extend([
                "Continue regular prenatal check-ups.",
                "Maintain a healthy and balanced diet.",
                "Stay hydrated.",
                "Continue routine fetal monitoring.",
                "Follow your doctor's advice."
            ])

        elif result == "Suspect":

            details.extend([
                "Schedule additional prenatal check-ups.",
                "Monitor fetal movements regularly.",
                "Follow your doctor's recommendations.",
                "Maintain a healthy lifestyle.",
                "Report any unusual symptoms immediately."
            ])

        else:

            details.extend([
                "Seek immediate medical attention.",
                "Continuous fetal monitoring is recommended.",
                "Attend all prenatal appointments.",
                "Follow your doctor's instructions strictly.",
                "Do not delay treatment if symptoms worsen."
            ])

        generate_pdf(
            "fetal_report.pdf",
            "Fetal Health Prediction Report",
            details
        )

        with open("fetal_report.pdf", "rb") as pdf_file:

            st.download_button(
                label="📄 Download Prediction Report",
                data=pdf_file,
                file_name="Fetal_Health_Report.pdf",
                mime="application/pdf"
            )

# ======================================================
# ABOUT PROJECT
# ======================================================


elif page == "About Project":

    st.title("ℹ️ About MaterniSense")

    st.image("images/home_banner.png", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background-color:#FFF5F7;
        padding:25px;
        border-radius:15px;
        border-left:8px solid #C2185B;
        color:black;">

    <h2>🏥 MaterniSense</h2>

    <p style="font-size:18px;">
    MaterniSense is an AI-powered healthcare application that predicts
    Maternal Health Risk and Fetal Health Status using Machine Learning.
    </p>

    <p style="font-size:18px;">
    It assists healthcare professionals and expectant mothers in
    assessing pregnancy-related risks quickly and efficiently.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------
    # Technologies Used
    # -----------------------------
    st.subheader("🛠 Technologies Used")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background-color:#E3F2FD;
            padding:20px;
            border-radius:15px;
            border:2px solid #90CAF9;
            color:black;
            height:220px;">

        <h3 style="text-align:center;">💻 Python</h3>

        <ul>
            <li>NumPy</li>
            <li>Pandas</li>
            <li>Joblib</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background-color:#FCE4EC;
            padding:20px;
            border-radius:15px;
            border:2px solid #F48FB1;
            color:black;
            height:220px;">

        <h3 style="text-align:center;">🤖 Machine Learning</h3>

        <ul>
            <li>Scikit-Learn</li>
            <li>Decision Tree</li>
            <li>Random Forest</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background-color:#E8F5E9;
            padding:20px;
            border-radius:15px;
            border:2px solid #81C784;
            color:black;
            height:220px;">

        <h3 style="text-align:center;">🌐 Deployment</h3>

        <ul>
            <li>Streamlit</li>
            <li>CSS</li>
            <li>Python</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------
    # Model Performance
    # -----------------------------
    st.write("")

    st.subheader("📊 Model Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="
        background-color:#E8F5E9;
        padding:20px;
        border-radius:15px;
        border:2px solid #66BB6A;
        color:black;
        text-align:center;">
  
        <h3>👩 Maternal Health Model</h3>

        <hr>

        <h1 style="color:green;">81.77%</h1>

        <b>Algorithm:</b> Decision Tree

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
        background-color:#E3F2FD;
        padding:20px;
        border-radius:15px;
        border:2px solid #42A5F5;
        color:black;
        text-align:center;">
   
        <h3>👶 Fetal Health Model</h3>

        <hr>

        <h1 style="color:green;">94.60%</h1>

        <b>Algorithm:</b> Random Forest

        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # Key Features
    # -----------------------------
    st.write("")

    st.subheader("✨ Key Features")

    st.markdown("""
    <div style="
    background-color:#FFF8E1;
    padding:20px;
    border-radius:15px;
    border:2px solid #FFD54F;
    color:black;">

    <ul>
    <li>✅ AI-based Maternal Health Risk Prediction</li>
    <li>✅ AI-based Fetal Health Status Prediction</li>
    <li>✅ User-friendly Streamlit Interface</li>
    <li>✅ Real-time Prediction Results</li>
    <li>✅ Attractive Healthcare Dashboard</li>
    <li>✅ Built using Python, Scikit-Learn and Streamlit</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Developer
    # -----------------------------
    st.write("")

    st.subheader("👨‍💻 Developer")

    st.markdown("""
    <div style="
    background-color:#F3E5F5;
    padding:25px;
    border-radius:15px;
    border:2px solid #BA68C8;
    color:black;">

    <h3>Soumya Ranjan Samal</h3>

    <b>Project:</b> MaterniSense – Maternal & Fetal Health Prediction System<br><br>

    <b>Degree:</b> B.Tech – Computer Science & Engineering<br><br>

    <b>Technologies:</b><br>

    Python • Streamlit • Scikit-Learn • NumPy • Pandas • Joblib • CSS

    <br><br>

    <b>Machine Learning Models:</b>

    <ul>
    <li>Decision Tree – Maternal Health Prediction</li>
    <li>Random Forest – Fetal Health Prediction</li>
    </ul>

    <b>Purpose:</b><br>

    To assist healthcare professionals and expectant mothers by providing AI-powered maternal and fetal health predictions through an interactive web application.

    </div>
    """, unsafe_allow_html=True)