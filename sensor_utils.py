"""Validation utilities for AtmosIQ sensor CSV uploads."""
from io import BytesIO
import pandas as pd

COLUMNS = ("timestamp", "temperature_c", "humidity_pct")

def load_readings(source):
    try:
        frame = pd.read_csv(source, on_bad_lines="error")
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeError, ValueError) as exc:
        raise ValueError("Invalid CSV file. Export readings as UTF-8 CSV.") from exc
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    frame = frame.loc[:, list(COLUMNS)].copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    for name in COLUMNS[1:]:
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
    frame = frame.dropna(subset=list(COLUMNS))
    frame = frame[frame["temperature_c"].between(-40, 80) & frame["humidity_pct"].between(0, 100)]
    if frame.empty:
        raise ValueError("No valid sensor readings found.")
    return frame.sort_values("timestamp").reset_index(drop=True)
