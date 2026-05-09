import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="GlycoSense - Diabetes Risk Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Outfit:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"]{background:#06090F;font-family:'Outfit',sans-serif;color:#D8DDE8}
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse 80% 40% at 10% 0%,#091828 0%,transparent 60%),radial-gradient(ellipse 60% 30% at 90% 80%,#0a1f12 0%,transparent 60%),#06090F}
[data-testid="stHeader"]{background:transparent!important}
[data-testid="stDecoration"]{display:none}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:1.25rem 0;border-bottom:1px solid #0f1c2e;margin-bottom:0.5rem}
.logo{font-family:'Playfair Display',serif;font-size:1.35rem;color:#FFFFFF;letter-spacing:0.02em}
.logo span{color:#22C55E;font-style:italic}
.topbar-badge{font-size:0.68rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#1D6EAA;background:rgba(29,110,170,0.1);border:1px solid rgba(29,110,170,0.25);border-radius:100px;padding:0.3rem 0.85rem}
.hero{padding:3rem 0 2rem;max-width:580px}
.hero-eyebrow{font-size:0.7rem;font-weight:600;letter-spacing:0.25em;text-transform:uppercase;color:#22C55E;margin-bottom:1rem}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3.2rem);font-weight:600;line-height:1.1;color:#FFFFFF;margin-bottom:1rem}
.hero-title em{font-style:italic;color:#3B9EFF}
.hero-desc{font-size:0.9rem;font-weight:300;color:#5A6880;line-height:1.8}
.form-card{background:linear-gradient(160deg,#0C1420 0%,#080E18 100%);border:1px solid #111E33;border-radius:20px;padding:2rem;margin-bottom:1.25rem}
.sec-label{font-size:0.68rem;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:#2A6EBB;margin-bottom:1.5rem;display:flex;align-items:center;gap:0.6rem}
.sec-label::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,#111E33,transparent)}
.stSlider label,.stNumberInput label{font-size:0.73rem!important;font-weight:500!important;letter-spacing:0.1em!important;text-transform:uppercase!important;color:#556070!important}
[data-testid="stThumbValue"]{background:#3B9EFF!important;color:#fff!important;font-family:'Outfit',sans-serif!important;font-size:0.72rem!important;font-weight:600!important;border-radius:6px!important}
.stNumberInput input{background:#080E18!important;border:1px solid #111E33!important;border-radius:10px!important;color:#D8DDE8!important;font-family:'Outfit',sans-serif!important;font-size:1rem!important;font-weight:500!important}
.stButton > button{width:100%!important;background:linear-gradient(135deg,#145EA8 0%,#3B9EFF 100%)!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:0.95rem 2rem!important;font-family:'Outfit',sans-serif!important;font-size:0.82rem!important;font-weight:600!important;letter-spacing:0.15em!important;text-transform:uppercase!important;box-shadow:0 4px 28px rgba(59,158,255,0.2)!important;transition:all 0.3s!important;margin-top:0.75rem!important}
.stButton > button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 36px rgba(59,158,255,0.35)!important}
.result-wrap{border-radius:20px;padding:2rem;margin-bottom:1.25rem;text-align:center}
.result-positive{background:linear-gradient(160deg,#150808 0%,#1e0d0d 100%);border:1px solid #6B1A1A}
.result-negative{background:linear-gradient(160deg,#071410 0%,#0a1e14 100%);border:1px solid #145e30}
.verdict-label{font-size:0.68rem;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;border-radius:100px;padding:0.28rem 0.9rem;display:inline-block;margin-bottom:1.25rem}
.verdict-pos-label{color:#FF6B6B;background:rgba(255,107,107,0.12);border:1px solid rgba(255,107,107,0.28)}
.verdict-neg-label{color:#22C55E;background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.28)}
.verdict-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:600;margin-bottom:0.4rem}
.result-positive .verdict-title{color:#FF8080}
.result-negative .verdict-title{color:#4ADE80}
.verdict-sub{font-size:0.82rem;font-weight:300;color:#3A4A5E}
.prob-section{background:linear-gradient(160deg,#0C1420 0%,#080E18 100%);border:1px solid #111E33;border-radius:16px;padding:1.75rem;margin-bottom:1.25rem}
.prob-row{margin-bottom:1.25rem}
.prob-row:last-child{margin-bottom:0}
.prob-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.5rem}
.prob-name{font-size:0.73rem;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:#4A5A70}
.prob-pct-pos{font-size:1rem;font-weight:600;color:#FF6B6B}
.prob-pct-neg{font-size:1rem;font-weight:600;color:#22C55E}
.bar-track{height:6px;background:#0A1020;border-radius:100px;overflow:hidden;border:1px solid #111E33}
.bar-fill-pos{height:100%;border-radius:100px;background:linear-gradient(90deg,#991B1B,#FF6B6B)}
.bar-fill-neg{height:100%;border-radius:100px;background:linear-gradient(90deg,#166534,#22C55E)}
.summary-card{background:linear-gradient(160deg,#0C1420 0%,#080E18 100%);border:1px solid #111E33;border-radius:16px;padding:1.75rem}
.summary-row{display:flex;justify-content:space-between;align-items:center;padding:0.65rem 0;border-bottom:1px solid #0D1828}
.summary-row:last-child{border-bottom:none}
.summary-key{font-size:0.73rem;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;color:#3A4A60}
.summary-val{font-size:0.88rem;font-weight:500;color:#A8B4C8}
.idle-card{background:linear-gradient(160deg,#0C1420 0%,#080E18 100%);border:1px solid #0D1828;border-radius:20px;padding:3.5rem 2rem;text-align:center;min-height:320px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.idle-title{font-family:'Playfair Display',serif;font-size:1.1rem;color:#1E2E42;margin-bottom:0.5rem}
.idle-sub{font-size:0.78rem;color:#141E2C;line-height:1.8;max-width:200px}
.footer{font-size:0.7rem;color:#151F2E;text-align:center;padding:2.5rem 0 1.5rem;line-height:2;letter-spacing:0.05em}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()
COLS = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

st.markdown(
    '<div class="topbar">'
    '<div class="logo">Glyco<span>Sense</span></div>'
    '<div class="topbar-badge">Clinical Risk Engine</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero">'
    '<div class="hero-eyebrow">Predictive Diagnostics</div>'
    '<div class="hero-title">Diabetes <em>Risk</em><br>Assessment Tool</div>'
    '<div class="hero-desc">KNN-based classification model trained on 614 clinical records. '
    'Adjust patient parameters to generate an evidence-informed risk profile.</div>'
    '</div>',
    unsafe_allow_html=True
)

col_left, col_gap, col_right = st.columns([5, 0.3, 4])

with col_left:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Patient Demographics</div>', unsafe_allow_html=True)

    dc1, dc2 = st.columns(2)
    with dc1:
        pregnancies = st.slider("Pregnancies", min_value=0, max_value=15, value=2, step=1)
    with dc2:
        age = st.slider("Age (years)", min_value=21, max_value=72, value=33, step=1)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Biochemical Markers</div>', unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        glucose = st.slider("Glucose (mg/dL)", min_value=44, max_value=198, value=120, step=1)
        insulin = st.slider("Insulin (mu U/ml)", min_value=15, max_value=846, value=80, step=1)
    with bc2:
        bmi = st.slider("BMI (kg/m2)", min_value=18.2, max_value=67.1, value=28.0, step=0.1)
        dpf = st.slider("Diabetes Pedigree", min_value=0.084, max_value=2.329, value=0.500, step=0.001)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Physical Measurements</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        blood_pressure = st.slider("Blood Pressure (mm Hg)", min_value=24, max_value=122, value=70, step=1)
    with pc2:
        skin_thickness = st.slider("Skin Thickness (mm)", min_value=7, max_value=99, value=25, step=1)

    st.markdown('</div>', unsafe_allow_html=True)
    run = st.button("Generate Risk Assessment")

with col_right:
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    if run:
        input_df = pd.DataFrame(
            [[pregnancies, glucose, blood_pressure, skin_thickness,
              insulin, bmi, dpf, age]],
            columns=COLS
        )
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0]
        risk_pct = round(prob[1] * 100, 1)
        safe_pct = round(prob[0] * 100, 1)

        if pred == 1:
            verdict_text  = "Diabetes Detected"
            verdict_sub   = "Risk indicators present - clinical follow-up advised."
            wrap_cls      = "result-wrap result-positive"
            label_cls     = "verdict-label verdict-pos-label"
            label_text    = "High Risk"
        else:
            verdict_text  = "No Diabetes"
            verdict_sub   = "No significant risk indicators found in this profile."
            wrap_cls      = "result-wrap result-negative"
            label_cls     = "verdict-label verdict-neg-label"
            label_text    = "Low Risk"

        result_html = (
            '<div class="{wrap}">'
            '<div class="{lbl_cls}">{lbl}</div>'
            '<div class="verdict-title">{title}</div>'
            '<div class="verdict-sub">{sub}</div>'
            '</div>'
        ).format(wrap=wrap_cls, lbl_cls=label_cls, lbl=label_text,
                 title=verdict_text, sub=verdict_sub)
        st.markdown(result_html, unsafe_allow_html=True)

        prob_html = (
            '<div class="prob-section">'
            '<div class="sec-label" style="margin-bottom:1.25rem">Probability Breakdown</div>'
            '<div class="prob-row">'
            '<div class="prob-header">'
            '<span class="prob-name">Diabetes Risk</span>'
            '<span class="prob-pct-pos">{rp}%</span>'
            '</div>'
            '<div class="bar-track"><div class="bar-fill-pos" style="width:{rp}%"></div></div>'
            '</div>'
            '<div class="prob-row">'
            '<div class="prob-header">'
            '<span class="prob-name">Non-Diabetic</span>'
            '<span class="prob-pct-neg">{sp}%</span>'
            '</div>'
            '<div class="bar-track"><div class="bar-fill-neg" style="width:{sp}%"></div></div>'
            '</div>'
            '</div>'
        ).format(rp=risk_pct, sp=safe_pct)
        st.markdown(prob_html, unsafe_allow_html=True)

        glucose_cat    = "Normal" if glucose < 100 else ("Pre-Diabetic" if glucose < 126 else "High")
        bmi_cat        = "Underweight" if bmi < 18.5 else ("Normal" if bmi < 25 else ("Overweight" if bmi < 30 else "Obese"))
        bp_cat         = "Normal" if blood_pressure < 80 else ("Elevated" if blood_pressure < 90 else "High")
        insulin_cat    = "Low" if insulin < 16 else ("Normal" if insulin < 166 else "High")
        dpf_cat        = "Low" if dpf < 0.5 else ("Moderate" if dpf < 1.0 else "High")
        age_cat        = "Young Adult" if age < 35 else ("Middle-Aged" if age < 55 else "Senior")

        def srow(key, val):
            return (
                '<div class="summary-row">'
                '<span class="summary-key">{k}</span>'
                '<span class="summary-val">{v}</span>'
                '</div>'
            ).format(k=key, v=val)

        summary_html = (
            '<div class="summary-card">'
            '<div class="sec-label" style="margin-bottom:1.25rem">Clinical Summary</div>'
            + srow("Glucose Level", "{} ({} mg/dL)".format(glucose_cat, glucose))
            + srow("BMI Category", "{} ({} kg/m2)".format(bmi_cat, round(bmi, 1)))
            + srow("Blood Pressure", "{} ({} mm Hg)".format(bp_cat, blood_pressure))
            + srow("Insulin Level", "{} ({} mu U/ml)".format(insulin_cat, insulin))
            + srow("Pedigree Risk", "{} ({})".format(dpf_cat, round(dpf, 3)))
            + srow("Age Group", "{} ({} yrs)".format(age_cat, age))
            + srow("Pregnancies", str(pregnancies))
            + '</div>'
        )
        st.markdown(summary_html, unsafe_allow_html=True)

    else:
        st.markdown(
            '<div class="idle-card">'
            '<div class="idle-title">No Assessment Yet</div>'
            '<div class="idle-sub">Set patient parameters and run the assessment to view results.</div>'
            '</div>',
            unsafe_allow_html=True
        )

st.markdown(
    '<div class="footer">'
    'For clinical decision support purposes only &nbsp;·&nbsp; Not a substitute for professional medical diagnosis<br>'
    'Model: K-Nearest Neighbours (k=5) &nbsp;·&nbsp; Training Set: 614 records &nbsp;·&nbsp; scikit-learn'
    '</div>',
    unsafe_allow_html=True
)
