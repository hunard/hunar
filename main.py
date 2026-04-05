"""
Simple Streamlit demo: a fake temperature sensor with random noise errors
and a simulated communication protocol (SPI / I2C / UART).
Run with: streamlit run main.py
"""

import random

import streamlit as st

# Built-in error tendency for each bus type (0 = never fails from protocol alone, 1 = always)
PROTOCOLS = {
    "SPI": {
        "error_rate": 0.1,
        "note": "High speed, low error.",
    },
    "I2C": {
        "error_rate": 0.3,
        "note": "Moderate speed; supports multiple devices on one bus.",
    },
    "UART": {
        "error_rate": 0.5,
        "note": "Simple wiring, but a higher error rate.",
    },
}

st.title("Temperature sensor simulator")
st.write(
    "Pick a **communication protocol** and a **Noise Level**. "
    "Together they decide how often a reading fails."
)

protocol = st.selectbox("Communication protocol", options=["SPI", "I2C", "UART"])
p_protocol = PROTOCOLS[protocol]["error_rate"]

st.write(f"**Using protocol:** {protocol}")
st.caption(PROTOCOLS[protocol]["note"])

noise_level = st.slider("Noise Level", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

# Combine protocol errors with environmental noise (independent chances → one formula)
p_fail = 1 - (1 - p_protocol) * (1 - noise_level)
st.caption(
    f"Each reading has about a **{p_fail * 100:.0f}%** chance to fail "
    f"(protocol **{protocol}** and noise slider combined)."
)

if st.button("Take reading"):
    if random.random() < p_fail:
        st.write("**Sensor output:** ERROR")
        st.error(
            f"Reading failed over **{protocol}**. "
            "The link and/or noise corrupted the data—no valid temperature."
        )
    else:
        temperature = round(random.uniform(18.0, 26.0), 1)
        st.write(f"**Sensor output:** {temperature} °C")
        st.success(f"OK — temperature is **{temperature} °C** (read successfully via **{protocol}**).")

