import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Digital Twin Simulator",
    page_icon="⚙️",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}

h1, h2, h3 {
    color: #ffffff;
}

div[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
}

div[data-testid="stMetricValue"] {
    color: #38bdf8;
}
div[data-testid="stMetricLabel"] {
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

div[data-testid="stMetric"] label {
    color: #ffffff !important;
}

.stButton button {
    background-color: #2563eb;
    color: white !important;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    font-weight: bold;
    min-height: 45px;
}
.stDownloadButton button {
    background-color: #2563eb !important;
    color: white !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 8px;
    font-weight: bold;
    min-height: 45px;
}

.stDownloadButton button:hover {
    background-color: #1d4ed8 !important;
    color: white !important;
}

.stDownloadButton button p {
    color: white !important;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white !important;
    border: 1px solid #60a5fa;
}

.stButton button p {
    color: white !important;
}
}
.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}

h1, h2, h3 {
    color: #38bdf8 !important;
}

div[data-testid="stMetric"] {
    background-color: #17243a;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricValue"] {
    color: #38bdf8;
}

div[data-testid="stMetricLabel"] {
    color: #e2e8f0;
}

button[kind="primary"] {
    background-color: #0284c7;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# Initialize simulation values
if "running" not in st.session_state:
    st.session_state.running = False

if "step" not in st.session_state:
    st.session_state.step = 0

if "temperature" not in st.session_state:
    st.session_state.temperature = 65.0

if "vibration" not in st.session_state:
    st.session_state.vibration = 3.2

if "rpm" not in st.session_state:
    st.session_state.rpm = 1200

if "history" not in st.session_state:
    st.session_state.history = []
    temperature = st.session_state.temperature
vibration = st.session_state.vibration
if "last_report" not in st.session_state:
    st.session_state.last_report = None

if "highest_severity" not in st.session_state:
    st.session_state.highest_severity = "Normal"

# Page heading
st.title("🏭 Smart Conveyor Digital Twin")
st.caption("REAL-TIME INDUSTRIAL MONITORING & PREDICTIVE MAINTENANCE SYSTEM")
st.markdown("---")
st.info("""
This project demonstrates a software-based Digital Twin of a conveyor belt system.
It monitors simulated temperature, vibration and RPM values to identify abnormal
operating conditions and demonstrate predictive maintenance.
""")
st.subheader("Manufacturing Conveyor Belt Monitoring System")
st.caption("DIGITAL TWIN | INDUSTRIAL MONITORING SYSTEM")

col1, col2, col3 = st.columns(3)

col1.info("Machine: Conveyor Belt")
col2.info("System: Digital Twin")
col3.info("Mode: Software Simulation")

st.write("Software-based virtual machine monitoring and simulation.")

st.markdown("---")
st.markdown("### ⚙️ Conveyor Operating Status")

if st.session_state.running:
    st.success("🟢 CONVEYOR STATUS: RUNNING")
else:
    st.error("🔴 CONVEYOR STATUS: STOPPED")
    st.markdown("---")
st.subheader("⚙️ Machine Specifications")

col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

col1.metric("Machine Type", "Conveyor")
col2.metric("Drive System", "Electric Motor")
col3.metric("Monitoring", "Real-time Simulation")
col4.metric("Sensors", "3 Virtual Sensors")
st.markdown("---")
st.subheader("🏭 3D Conveyor Belt Visualization")

model_path = "models/model conveyor belt.glb"

with open(model_path, "rb") as f:
    model_data = base64.b64encode(f.read()).decode("utf-8")

animation_control = "autoplay" if st.session_state.running else ""
model_html = f"""
<script type="module"
src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js">
</script>

<model-viewer
    src="data:model/gltf-binary;base64,{model_data}"
    camera-controls
    {animation_control}
    
    
    shadow-intensity="1"
    style="width:100%; height:450px; background-color:#1e293b; border-radius:12px;">
</model-viewer>
"""

components.html(model_html, height=470)






# Simulation controls
st.header("Machine Simulation")

fault = st.selectbox(
    "Select Operating Condition",
    [
        "Normal Operation",
        "Bearing Fault",
        "Motor Overheating",
        "Excessive Vibration"
    ]
)


    

col1, col2, col3 = st.columns(3)

if col1.button("▶ Start Simulation", use_container_width=True):
    st.session_state.running = True

with col2:
    if st.button("Stop Simulation", use_container_width=True):
        st.session_state.running = False

        history_df = pd.DataFrame(st.session_state.history)

        if not history_df.empty:
            st.session_state.last_report = {
                "Temperature": st.session_state.temperature,
"Vibration": st.session_state.vibration,
"RPM": st.session_state.rpm,
"Final Condition": (
    "Critical" if st.session_state.temperature >= 90 or st.session_state.vibration >= 10
    else "Warning" if st.session_state.temperature >= 80 or st.session_state.vibration >= 7
    else "Normal"
),
                "Highest Severity": st.session_state.highest_severity,
                "Total Readings": len(history_df)
            }

        st.rerun()

if col3.button("🔄 Reset Simulation", use_container_width=True):
    st.session_state.running = False
    st.session_state.step = 0
    st.session_state.temperature = 65.0
    st.session_state.vibration = 3.2
    st.session_state.rpm = 1200
    st.session_state.history = []
    st.rerun()

if st.session_state.running:
    st_autorefresh(interval=2000, key="machine_refresh")

    st.session_state.step += 1
    step = st.session_state.step

    # Generate simulated sensor readings
    if fault == "Normal Operation":
        temperature = 65 + np.random.uniform(-1, 2)
        vibration = 3.2 + np.random.uniform(-0.3, 0.3)
        rpm = 1200 + np.random.randint(-10, 11)

    elif fault == "Bearing Fault":
        temperature = 65 + min(step * 0.5, 25)
        vibration = 3.2 + min(step * 0.18, 8)
        rpm = 1200 - min(step * 3, 300)

    elif fault == "Motor Overheating":
        temperature = 65 + min(step * 1.2, 45)
        vibration = 3.2 + min(step * 0.03, 2)
        rpm = 1200 - min(step * 2, 250)

    else:
        temperature = 65 + min(step * 0.1, 10)
        vibration = 3.2 + min(step * 0.3, 10)
        rpm = 1200 - min(step * 4, 300)

    st.session_state.temperature = round(float(temperature), 2)
    st.session_state.vibration = round(float(vibration), 2)
    st.session_state.rpm = int(rpm)

    # Store readings
    st.session_state.history.append({
        "Time": step,
        "Temperature": st.session_state.temperature,
        "Vibration": st.session_state.vibration,
        "RPM": st.session_state.rpm
    })

    # Keep latest 60 readings
    st.session_state.history = st.session_state.history[-60:]

if st.session_state.running:
    st.info("Simulation is running. Readings update every 2 seconds.")
else:
    st.info("Simulation is stopped. Press Start Simulation to begin.")

st.markdown("---")

# Current machine readings
st.header("Live Machine Parameters")
col1, col2, col3 = st.columns(3)

col1.metric(
    "Temperature",
    f"{st.session_state.temperature} °C"
)
col2.metric(
    "Vibration",
    f"{st.session_state.vibration}mm/s"
)



col3.metric(
    "Motor Speed",
    f"{st.session_state.rpm} RPM"
)
st.markdown("---")
temperature = st.session_state.temperature
vibration = st.session_state.vibration
current_severity = (
    "Critical" if temperature >= 90 or vibration >= 10
    else "Warning" if temperature >= 80 or vibration >= 7
    else "Normal"
)

severity_order = {"Normal": 1, "Warning": 2, "Critical": 3}

if severity_order[current_severity] > severity_order[st.session_state.highest_severity]:
    st.session_state.highest_severity = current_severity
st.subheader("📊 Overall Machine Condition")

if temperature >= 90 or vibration >= 10:
    st.error("🔴 CRITICAL CONDITION")

elif temperature >= 80 or vibration >= 7:
    st.warning("🟡 ATTENTION REQUIRED")

else:
    st.success("🟢 MACHINE HEALTHY")

# Machine health
st.header("Machine Health Status")

temperature = st.session_state.temperature
vibration = st.session_state.vibration

if temperature >= 90 or vibration >= 10:
    st.error("CRITICAL - Immediate maintenance required")

elif temperature >= 80 or vibration >= 7:
    st.warning("WARNING - Machine needs inspection")

else:
    st.success("NORMAL - Machine operating properly")

# Predictive maintenance risk estimate
temperature_risk = max(0, min(100, (temperature - 60) / 40 * 100))
vibration_risk = max(0, min(100, (vibration - 3) / 9 * 100))

failure_risk = (temperature_risk + vibration_risk) / 2

st.header("Predictive Maintenance")

st.metric("Estimated Failure Risk", f"{failure_risk:.1f}%")

if failure_risk <= 30:
    st.success("LOW RISK - Continue routine monitoring")

elif failure_risk <= 60:
    st.warning("MODERATE RISK - Inspect the machine")

else:
    st.error("HIGH RISK - Maintenance attention required")
    # Maintenance Recommendations
    st.markdown("---")
st.header("🔧 Maintenance Recommendations")

if temperature >= 80 or vibration >= 7:

    if temperature >= 90 or vibration >= 10:
        st.error("🔴 CRITICAL CONDITION: Immediate maintenance required.")

    else:
        st.warning("🟡 WARNING: Abnormal machine parameters detected.")

    if fault == "Bearing Fault":
        st.write("**Recommended Actions:**")
        st.write("- Inspect bearing condition.")
        st.write("- Check bearing lubrication.")
        st.write("- Monitor vibration levels.")
        st.write("- Check bearing wear and damage.")
        st.write("- Replace damaged bearings if necessary.")

    elif fault == "Motor Overheating":
        st.write("**Recommended Actions:**")
        st.write("- Inspect the motor cooling system.")
        st.write("- Check motor load and current.")
        st.write("- Inspect ventilation openings.")
        st.write("- Check for excessive friction.")
        st.write("- Allow the motor to cool if necessary.")

    elif fault == "Excessive Vibration":
        st.write("**Recommended Actions:**")
        st.write("- Check pulley alignment.")
        st.write("- Inspect conveyor belt tension.")
        st.write("- Check loose mounting bolts.")
        st.write("- Inspect bearings and rotating components.")
        st.write("- Check for mechanical imbalance.")

else:
    st.success("🟢 MACHINE HEALTHY")
    st.write("No immediate maintenance action required.")







    
st.markdown("---")
st.header("🏗️ Digital Twin System Architecture")

st.subheader("System Workflow")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📡 **Virtual Sensors**\n\nTemperature, Vibration and RPM")

with col2:
    st.info("⚙️ **Simulation Engine**\n\nPython-based sensor simulation")

with col3:
    st.info("📊 **Monitoring Dashboard**\n\nMachine health and predictive maintenance")

st.markdown("**Workflow:**")

st.write(
    "Virtual Sensors → Data Collection → Simulation Engine "
    "→ Condition Monitoring → Fault Detection → Maintenance Alerts"
)

# Historical graphs
st.markdown("---")
st.header("Machine Monitoring History")

if st.session_state.history:
    data = pd.DataFrame(st.session_state.history)
    st.download_button(
    label="📥 Download Sensor Data",
    data=data.to_csv(index=False),
    file_name="conveyor_sensor_data.csv",
    mime="text/csv"
)

    fig1 = px.line(
        data,
        x="Time",
        y="Temperature",
        markers=True,
        title="Temperature vs Time"
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        data,
        x="Time",
        y="Vibration",
        markers=True,
        title="Vibration vs Time"
    )
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(
        data,
        x="Time",
        y="RPM",
        markers=True,
        title="Motor Speed vs Time"
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.write("Start the simulation to generate machine history.")

st.markdown("---")
st.caption("Digital Twin Project | Software Simulation Prototype")
st.markdown("---")
st.header("📋 Simulation Analysis Report")

if st.session_state.last_report is not None:

    report = st.session_state.last_report

    col1, col2, col3 = st.columns(3)

    col1.metric("Temperature", f"{report['Temperature']:.2f} °C")
    col2.metric("Vibration", f"{report['Vibration']:.2f} mm/s")
    col3.metric("Motor Speed", f"{report['RPM']} RPM")

    st.write("**Final Machine Condition:**", report["Final Condition"])
    st.write("**Highest Severity Reached:**", report["Highest Severity"])
    st.write("**Total Sensor Readings:**", report["Total Readings"])

else:
    st.info("Start and stop the simulation to generate an analysis report.")




