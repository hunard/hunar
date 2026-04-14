"""
Smart Factory Communication Simulator — Streamlit demo.

Simulates a temperature sensor over SPI / I2C / UART with noise, retries,
and running metrics. Run with: streamlit run main.py
"""

import random

import streamlit as st

# --- Page setup (must be the first Streamlit command) ---
st.set_page_config(
    page_title="Smart Factory Communication Simulator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# First try + up to 3 retries if each packet is corrupted
MAX_RETRIES = 3
MAX_ATTEMPTS = 1 + MAX_RETRIES


def init_session_state() -> None:
    """Persist counters, chart series, and last transmission summary across reruns."""
    if "total_tx" not in st.session_state:
        st.session_state.total_tx = 0
        st.session_state.successful_tx = 0
        st.session_state.failed_tx = 0
        st.session_state.cum_success_series = []
        st.session_state.cum_fail_series = []
        st.session_state.last_event = None


init_session_state()

# SPI / I2C / UART base error rates (combined with noise later)
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

# =============================================================================
# Title
# =============================================================================
st.title("Smart Factory Communication Simulator")
st.caption(
    "Industrial-style dashboard: configure the link, run a read with automatic retries, "
    "and monitor cumulative communication health."
)

# =============================================================================
# System Controls
# =============================================================================
st.header("System Controls")
st.write(
    "Set environmental **noise**, choose **Manual** or **Auto** protocol routing, then request a sensor read."
)

mode = st.radio(
    "Mode",
    options=["Manual Mode", "Auto Mode"],
    horizontal=True,
)
st.caption(f"**Active mode:** {mode}")

noise_level = st.slider(
    "Environmental noise (0 = calm, 1 = harsh)",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05,
)

# Manual: operator picks the bus. Auto: bus follows noise thresholds.
protocol: str
auto_selection_note: str | None = None
if mode == "Manual Mode":
    protocol = st.selectbox("Communication protocol", options=["SPI", "I2C", "UART"])
else:
    if noise_level < 0.3:
        protocol = "SPI"
        auto_selection_note = (
            "Auto selected **SPI** — noise is **below 0.3** (favor fast, low-error link)."
        )
    elif noise_level <= 0.6:
        protocol = "I2C"
        auto_selection_note = (
            "Auto selected **I2C** — noise is **between 0.3 and 0.6** (balanced bus)."
        )
    else:
        protocol = "UART"
        auto_selection_note = (
            "Auto selected **UART** — noise is **above 0.6** "
            "(simple serial; higher base error rate)."
        )

p_protocol = PROTOCOLS[protocol]["error_rate"]
# Same formula as before: one probability per attempt from protocol + noise
p_fail = 1 - (1 - p_protocol) * (1 - noise_level)

take_reading = st.button("Take reading", type="primary", use_container_width=True)

if take_reading:
    temperature = None
    success = False
    retries_used = 0

    for _attempt in range(1, MAX_ATTEMPTS + 1):
        st.session_state.total_tx += 1
        if random.random() < p_fail:
            st.session_state.failed_tx += 1
        else:
            st.session_state.successful_tx += 1
            success = True
            temperature = round(random.uniform(18.0, 26.0), 1)
            retries_used = _attempt - 1
            break

    st.session_state.cum_success_series.append(st.session_state.successful_tx)
    st.session_state.cum_fail_series.append(st.session_state.failed_tx)

    if success:
        sensor_out = f"{temperature} °C"
        if retries_used > 0:
            msg = (
                f"**Recovered after retry** — valid frame on **{protocol}** after "
                f"**{retries_used}** corrupted packet(s). Temperature **{temperature} °C**."
            )
        else:
            msg = (
                f"**Transmission successful** on **{protocol}**. Temperature **{temperature} °C**."
            )
        st.session_state.last_event = {
            "sensor_output": sensor_out,
            "ok": True,
            "message": msg,
        }
    else:
        st.session_state.last_event = {
            "sensor_output": "ERROR",
            "ok": False,
            "message": (
                f"**All attempts failed** on **{protocol}** after **{MAX_ATTEMPTS}** tries "
                "(packet corrupted each time). No valid temperature."
            ),
        }

# =============================================================================
# Communication Status
# =============================================================================
st.header("Communication Status")

if mode == "Auto Mode" and auto_selection_note:
    st.info(auto_selection_note)

col_a, col_b = st.columns(2)
with col_a:
    st.metric("Active protocol", protocol)
with col_b:
    st.metric("Estimated corrupt probability (per attempt)", f"{p_fail * 100:.0f}%")

st.caption(PROTOCOLS[protocol]["note"])
st.caption(
    f"Each attempt fails with about **{p_fail * 100:.0f}%** probability "
    f"(**{protocol}** baseline plus environmental noise). "
    f"Up to **{MAX_RETRIES}** retries after the first send."
)

st.subheader("Last transmission")
if st.session_state.last_event is None:
    st.warning("No transmission yet — use **Take reading** in System Controls.")
else:
    ev = st.session_state.last_event
    st.write(f"**Sensor output:** {ev['sensor_output']}")
    if ev["ok"]:
        st.success(ev["message"])
    else:
        st.error(ev["message"])

# =============================================================================
# System Metrics
# =============================================================================
st.header("System Metrics")
st.caption("Counters update after each **Take reading**. Chart uses cumulative totals per reading.")

m1, m2, m3 = st.columns(3)
m1.metric("Total transmissions", st.session_state.total_tx)
m2.metric("Successful transmissions", st.session_state.successful_tx)
m3.metric("Failed transmissions", st.session_state.failed_tx)

if st.session_state.cum_success_series:
    st.subheader("Success vs failure over time")
    st.line_chart(
        {
            "Successful (cumulative)": st.session_state.cum_success_series,
            "Failed (cumulative)": st.session_state.cum_fail_series,
        }
    )
else:
    st.info("Run a transmission to populate the trend chart.")
