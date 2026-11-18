import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from io import StringIO
from sensor_utils import load_readings

st.set_page_config(page_title="AtmosIQ IoT",page_icon="🌡️",layout="wide")
st.title("🌡️ AtmosIQ — Environmental Monitoring")
st.caption("Arduino DHT11 compatible • Simulation mode and CSV logger support")
mode = st.radio("Data source",["Simulated demo","Logged CSV"],horizontal=True)
if mode == "Simulated demo":
    rng = np.random.default_rng(8)
    t = pd.date_range(end=pd.Timestamp.now(),periods=120,freq="min")
    df = pd.DataFrame({"timestamp":t,"temperature_c":(27+2*np.sin(np.arange(120)/14)+rng.normal(0,.3,120)).round(1),"humidity_pct":(56+7*np.cos(np.arange(120)/19)+rng.normal(0,1,120)).round(1)})
    st.warning("Showing simulated sensor readings, not measurements from physical hardware.")
else:
    upload = st.file_uploader("Upload a CSV from serial_logger.py",type="csv")
    if upload:
        source = upload
    elif Path("sample_data/sensor_readings.csv").exists():
        source = "sample_data/sensor_readings.csv"
        st.info("Showing bundled sample readings.")
    else:
        st.info("Upload a CSV with timestamp, temperature_c, humidity_pct.")
        st.stop()
try:
    if mode == "Logged CSV":
        if upload and upload.size > 2_000_000:
            st.error("CSV upload must be 2 MB or smaller.")
            st.stop()
        df = load_readings(source)
    else:
        df = load_readings(StringIO(df.to_csv(index=False)))
except (ValueError, OSError) as exc:
    st.error(str(exc))
    st.stop()
latest = df.iloc[-1]
a,b,c = st.columns(3)
a.metric("Temperature",f"{latest.temperature_c:.1f} °C")
b.metric("Humidity",f"{latest.humidity_pct:.1f}%")
c.metric("Readings",len(df))
if latest.temperature_c > 35:
    st.error("High temperature alert (above 35 °C)")
elif latest.humidity_pct > 75:
    st.warning("High humidity alert (above 75%)")
else:
    st.success("Readings within configured demo alert thresholds")
left,right = st.columns(2)
with left:
    st.plotly_chart(px.line(df,x="timestamp",y="temperature_c",title="Temperature trend"),use_container_width=True)
with right:
    st.plotly_chart(px.line(df,x="timestamp",y="humidity_pct",title="Humidity trend"),use_container_width=True)
st.dataframe(df.tail(30),use_container_width=True)
st.download_button("Download readings",df.to_csv(index=False),"atmosiq_readings.csv","text/csv")
