import streamlit as st

# ======================================================
# HOME PAGE
# ======================================================
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
    Background:#F5F9FF;
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