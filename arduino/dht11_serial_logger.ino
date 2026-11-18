// Install the Adafruit DHT Sensor Library in Arduino IDE.
// DHT11 DATA -> Arduino Uno D2; VCC -> 5V; GND -> GND.
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
void setup() {
  Serial.begin(9600);
  dht.begin();
}
void loop() {
  delay(2000);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)) {
    // Skip failed reads; Python logger expects numeric CSV.
    return;
  }
  Serial.print(temperature, 1);
  Serial.print(",");
  Serial.println(humidity, 1);
}
