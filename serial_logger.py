"""Read Arduino CSV serial lines: temperature_c,humidity_pct."""
import csv
import argparse
from datetime import datetime
import serial
import math

parser = argparse.ArgumentParser()
parser.add_argument("--port",required=True,help="Example: COM3 or /dev/ttyUSB0")
parser.add_argument("--baud",type=int,default=9600)
parser.add_argument("--output",default="readings.csv")
args = parser.parse_args()
with serial.Serial(args.port,args.baud,timeout=3) as device, open(args.output,"a",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["timestamp","temperature_c","humidity_pct"])
    print("Logging readings. Press Ctrl+C to stop.")
    try:
        while True:
            line = device.readline().decode("utf-8",errors="replace").strip()
            try:
                temp,humidity = (float(x) for x in line.split(","))
                if math.isfinite(temp) and math.isfinite(humidity) and -40 <= temp <= 80 and 0 <= humidity <= 100:
                    writer.writerow([datetime.now().isoformat(timespec="seconds"),temp,humidity])
                    file.flush()
                    print(temp,humidity)
            except (ValueError,TypeError):
                continue
    except KeyboardInterrupt:
        print("Stopped.")
