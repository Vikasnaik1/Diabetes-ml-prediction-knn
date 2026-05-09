import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="DiabeteIQ — Clinical Risk Assessment",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #070B14;
    font-family: 'DM Sans', sans-serif;
    color: #E8EAF0;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0d1f3c 0%, #070B14 60%);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent; }

.hero-section {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
}

.hero-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #4A9EFF;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 400;
    line-height: 1.1;
    color: #FFFFFF;
    margin-bottom: 1rem;
}

.hero-title span {
    font-style: italic;
    color: #4A9EFF;
}

.hero-sub {
    font-size: 0.95rem;
    color: #7A8599;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E2D4A, transparent);
    margin: 2rem 0;
}

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #C8D0E0;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1A2540;
}

.card {
    background: linear-gradient(135deg, #0D1526 0%, #0A1020 100%);
    border: 1px solid #1A2540;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.3s;
}

.card:hover { border-color: #2A3D60; }

.stNumberInput label, .stSlider label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #6A7A99 !important;
    margin-bottom: 0.4rem !important;
}

.stNumberInput input {
    background: #0A1020 !important;
    border: 1px solid #1E2D4A !important;
    border-radius: 10px !important;
    color: #E8EAF0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 0.9rem !important;
    transition: border-color 0.2s !important;
}

.stNumberInput input:focus {
    border-color: #4A9EFF !important;
    box-shadow: 0 0 0 3px rgba(74,158,255,0.1) !important;
}

.stSlider [data-baseweb="slider"] {
    margin-top: 0.5rem;
}

.stSlider [data-testid="stThumbValue"] {
    background: #4A9EFF !important;
    color: white !important;
    font-size: 0.75rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1A5CCC 0%, #4A9EFF 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(74,158,255,0.25) !important;
    margin-top: 1rem !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(74,158,255,0.4) !important;
}

.result-positive {
    background: linear-gradient(135deg, #1a0a0a 0%, #2d0f0f 100%);
    border: 1px solid #7B2020;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}

.result-negative {
    background: linear-gradient(135deg, #081a10 0%, #0d2a18 100%);
    border: 1px solid #1a5e32;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}

.result-verdict {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    margin-bottom: 0.5rem;
}

.result-positive .result-verdict { color: #FF6B6B; }
.result-negative .result-verdict { color: #4ADE80; }

.result-sub {
    font-size: 0.85rem;
    color: #7A8599;
    font-weight: 300;
}

.prob-bar-bg {
    background: #0D1526;
    border-radius: 100px;
    height: 8px;
    width: 100%;
    margin: 0.5rem 0;
    overflow: hidden;
    border: 1px solid #1A2540;
}

.prob-bar-fill-risk {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #CC3333, #FF6B6B);
    transition: width 1s ease;
}

.prob-bar-fill-safe {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #16A34A, #4ADE80);
    transition: width 1s ease;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #1A2540;
}

.metric-row:last-child { border-bottom: none; }

.metric-label {
    font-size: 0.78rem;
    color: #6A7A99;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.metric-value {
    font-size: 0.95rem;
    font-weight: 500;
    color: #C8D0E0;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.8rem;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.badge-high { background: rgba(255,107,107,0.15); color: #FF6B6B; border: 1px solid rgba(255,107,107,0.3); }
.badge-low  { background: rgba(74,222,128,0.15);  color: #4ADE80;  border: 1px solid rgba(74,222,128,0.3);  }

.footnote {
    font-size: 0.72rem;
    color: #3A4A62;
    text-align: center;
    margin-top: 3rem;
    padding-bottom: 2rem;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.markdown("""
<div class="hero-section">
    <div class="hero-label">Clinical Decision Support</div>
    <div class="hero-title">Diabetes <span>Risk</span> Assessment</div>
    <div class="hero-sub">
        Evidence-based prediction using K-Nearest Neighbour classification
        trained on the Pima Indians Diabetes dataset.
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

col_form, col_gap, col_result = st.columns([5, 0.4, 4])

with col_form:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Patient Profile</div>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
    with r1c2:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=30, step=1)

    st.markdown('<div class="divider" style="margin:1rem 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Clinical Measurements</div>', unsafe_allow_html=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        glucose = st.number_input("Glucose (mg/dL)", min_value=0, max_value=300, value=120, step=1)
        blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70, step=1)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20, step=1)
    with r2c2:
        insulin = st.number_input("Insulin (mu U/ml)", min_value=0, max_value=900, value=80, step=1)
        bmi = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=70.0, value=25.0, step=0.1, format="%.1f")
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.000, max_value=3.000, value=0.500, step=0.001, format="%.3f")

    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("Run Prediction Analysis")

with col_result:
    st.markdown('<div style="height: 1.5rem"></div>', unsafe_allow_html=True)

    if predict_clicked:
        input_df = pd.DataFrame([[pregnancies, glucose, blood_pressure, skin_thickness,
                                   insulin, bmi, dpf, age]],
                                 columns=['Pregnancies','Glucose','BloodPressure','SkinThickness',
                                          'Insulin','BMI','DiabetesPedigreeFunction','Age'])

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]

        risk_pct  = round(probability[1] * 100, 1)
        safe_pct  = round(probability[0] * 100, 1)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-positive">
                <div class="badge badge-high" style="margin-bottom:1rem">High Risk Detected</div>
                <div class="result-verdict">Diabetic</div>
                <div class="result-sub">Probability-based clinical flag</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-negative">
                <div class="badge badge-low" style="margin-bottom:1rem">Low Risk</div>
                <div class="result-verdict">Non-Diabetic</div>
                <div class="result-sub">No significant risk indicators found</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Probability Breakdown</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-bottom: 1.25rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
                <span style="font-size:0.78rem; color:#6A7A99; text-transform:uppercase; letter-spacing:0.08em;">Diabetic Risk</span>
                <span style="font-size:0.9rem; font-weight:600; color:#FF6B6B;">{risk_pct}%</span>
            </div>
            <div class="prob-bar-bg">
                <div class="prob-bar-fill-risk" style="width:{risk_pct}%"></div>
            </div>
        </div>
        <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
                <span style="font-size:0.78rem; color:#6A7A99; text-transform:uppercase; letter-spacing:0.08em;">Non-Diabetic</span>
                <span style="font-size:0.9rem; font-weight:600; color:#4ADE80;">{safe_pct}%</span>
            </div>
            <div class="prob-bar-bg">
                <div class="prob-bar-fill-safe" style="width:{safe_pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Input Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row"><span class="metric-label">Glucose</span><span class="metric-value">{glucose} mg/dL</span></div>
        <div class="metric-row"><span class="metric-label">BMI</span><span class="metric-value">{bmi} kg/m²</span></div>
        <div class="metric-row"><span class="metric-label">Blood Pressure</span><span class="metric-value">{blood_pressure} mm Hg</span></div>
        <div class="metric-row"><span class="metric-label">Insulin</span><span class="metric-value">{insulin} mu U/ml</span></div>
        <div class="metric-row"><span class="metric-label">Age</span><span class="metric-value">{age} years</span></div>
        <div class="metric-row"><span class="metric-label">Pedigree Function</span><span class="metric-value">{dpf:.3f}</span></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 3rem 2rem; min-height: 340px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="width:56px; height:56px; border-radius:50%; background:#0D1526; border:1px solid #1A2540; display:flex; align-items:center; justify-content:center; margin:0 auto 1.25rem; font-size:1.5rem;">⚕</div>
            <div style="font-family:'DM Serif Display',serif; font-size:1.1rem; color:#3A4A62; margin-bottom:0.5rem;">Awaiting Input</div>
            <div style="font-size:0.8rem; color:#2A3550; line-height:1.7; max-width:220px;">
                Complete the patient profile and run the analysis to view results.
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footnote">
    For clinical decision support purposes only. Not a substitute for professional medical diagnosis.<br>
    Model: K-Nearest Neighbours · Dataset: Pima Indians Diabetes · Algorithm: scikit-learn
</div>
""", unsafe_allow_html=True)
