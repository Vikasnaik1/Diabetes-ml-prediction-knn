import streamlit as st
import pickle
import numpy as np
 
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
 
st.set_page_config(page_title="Diabetes Prediction", layout="centered")
 
st.title("Diabetes Risk Prediction")
st.markdown("Enter patient details to predict the likelihood of diabetes.")
 
col1, col2 = st.columns(2)
 
with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
    glucose = st.number_input("Glucose (mg/dL)", min_value=0, max_value=300, value=120)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)
 
with col2:
    insulin = st.number_input("Insulin (mu U/ml)", min_value=0, max_value=900, value=80)
    bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, format="%.1f")
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5, format="%.3f")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
 
if st.button("Predict", use_container_width=True):
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                            insulin, bmi, dpf, age]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]
 
    st.divider()
 
    if prediction == 1:
        st.error("Prediction: Diabetic")
        st.metric("Probability of Diabetes", f"{probability[1] * 100:.1f}%")
    else:
        st.success("Prediction: Non-Diabetic")
        st.metric("Probability of No Diabetes", f"{probability[0] * 100:.1f}%")
 
    col_a, col_b = st.columns(2)
    col_a.metric("Non-Diabetic Probability", f"{probability[0] * 100:.1f}%")
    col_b.metric("Diabetic Probability", f"{probability[1] * 100:.1f}%")
