import streamlit as st
import pickle
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="centered"
)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 2rem; }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.6rem;
        border: none;
        border-radius: 10px;
    }
    .result-positive {
        background-color: #ffe8e8;
        border: 2px solid #e74c3c;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #c0392b;
        font-size: 1.2rem;
        font-weight: 700;
    }
    .result-negative {
        background-color: #e8f8ee;
        border: 2px solid #27ae60;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #1e8449;
        font-size: 1.2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🩺 Diabetes Risk Predictor")
st.caption("KNN Classifier · Pima Indians Diabetes Dataset · 8 Features")
st.markdown("---")

# ── Input form ────────────────────────────────────────────────────────────────
st.subheader("📋 Enter Patient Details")

col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
    glucose     = st.number_input("Glucose (mg/dL)", min_value=0, max_value=300, value=120)
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=200, value=70)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)

with col2:
    insulin     = st.number_input("Insulin (μU/mL)", min_value=0, max_value=900, value=80)
    bmi         = st.number_input("BMI", min_value=0.0, max_value=70.0, value=28.5, step=0.1, format="%.1f")
    dpf         = st.number_input("Diabetes Pedigree Function", min_value=0.000, max_value=3.000, value=0.470, step=0.001, format="%.3f")
    age         = st.number_input("Age", min_value=1, max_value=120, value=33)

st.markdown("---")

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("🔍 Predict"):
    features = np.array([[pregnancies, glucose, blood_pressure,
                          skin_thickness, insulin, bmi, dpf, age]])

    prediction   = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    prob_diabetic     = round(float(probabilities[1]) * 100, 1)
    prob_non_diabetic = round(float(probabilities[0]) * 100, 1)

    st.markdown("### 🧾 Prediction Result")

    if prediction == 1:
        st.markdown(f"""
        <div class="result-positive">
            ⚠️ High Risk of Diabetes<br>
            <span style="font-size:0.95rem; font-weight:400">
                Confidence: {prob_diabetic}%
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-negative">
            ✅ Low Risk of Diabetes<br>
            <span style="font-size:0.95rem; font-weight:400">
                Confidence: {prob_non_diabetic}%
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Probability bar chart
    st.markdown("#### 📊 Probability Breakdown")
    st.progress(int(prob_diabetic), text=f"Diabetic: {prob_diabetic}%")
    st.progress(int(prob_non_diabetic), text=f"Non-Diabetic: {prob_non_diabetic}%")

    # Details expander
    with st.expander("🔬 View Input Summary"):
        import pandas as pd
        input_df = pd.DataFrame({
            "Feature": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
            "Value": [pregnancies, glucose, blood_pressure, skin_thickness,
                      insulin, bmi, dpf, age]
        })
        st.dataframe(input_df, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Model: KNeighborsClassifier (K=5) · Built with Streamlit")
