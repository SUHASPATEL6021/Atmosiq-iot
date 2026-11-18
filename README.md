# 🌡️ AtmosIQ — IoT Environmental Monitoring

Streamlit dashboard for DHT11 temperature and humidity measurements, with a simulation mode that works without hardware.

## 🌐 Live demo
**[Open AtmosIQ IoT](https://suhas-atmosiq-iot.streamlit.app/)**

The hosted app supports simulated data and uploaded CSV logs. Physical Arduino serial logging must run locally.

## Features
- Demo mode with clearly labeled simulated readings
- CSV upload for real logged readings
- Temperature and humidity charts
- Configurable-in-code warning thresholds
- Arduino Uno sketch and Python serial logger

## Hardware
Arduino Uno + DHT11: DATA → D2, VCC → 5V, GND → GND. Install **Adafruit DHT Sensor Library** in Arduino IDE.

Upload `arduino/dht11_serial_logger.ino` to the board, then log data:
```bash
pip install -r requirements.txt
python serial_logger.py --port COM3 --output readings.csv
streamlit run app.py
```
Change COM3 to the appropriate port. Upload the generated CSV in the dashboard's Logged CSV mode.

## Notes
Simulated data is **not** real-time physical sensing. Hardware integration requires an Arduino, sensor, and serial connection.
