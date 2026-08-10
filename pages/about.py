import streamlit as st

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