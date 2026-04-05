"""
Simple Streamlit demo: a fake temperature sensor with random noise errors.
Run with: streamlit run main.py
"""

import random

import streamlit as st

st.title("Temperature sensor simulator")
st.write("Higher **Noise Level** means a higher chance the reading fails.")

noise_level = st.slider("Noise Level", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

if st.button("Take reading"):
    # Random chance of failure: same as the noise slider (0 = never, 1 = always)
    if random.random() < noise_level:
        st.error("ERROR — could not read temperature (noise interfered).")
    else:
        temperature = round(random.uniform(18.0, 26.0), 1)
        st.success(f"OK — temperature is **{temperature} °C**.")
