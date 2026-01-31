import streamlit as st
import joblib
import pandas as pd

model = joblib.load("fault_detector.pkl")

st.title("AI Circuit Fault detector")
st.write("upload your circuit gain and check fault")

gain = st.number_input("enter circuit gain", value=0.5)

if st.button("check"):
    sample = pd.DataFrame({"gain": [gain]})
    
    pred = model.predict(sample)[0]
    proba = model.predict_proba(sample)[0]
    confidence = max(proba) * 100

    if pred == 0:
        st.success("circuit ok")
    else:
        st.error("Fault detected")

    st.info(f"Confidence: {confidence:.2f}%")

    
    if len(proba) == 2:
        st.bar_chart({"OK": proba[0], "Fault": proba[1]})
    else:
        st.bar_chart({"OK": proba[0]})