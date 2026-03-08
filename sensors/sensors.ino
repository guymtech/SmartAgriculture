#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <DHT.h>

// Sensor Pins from your connection.json
#define DHTPIN 15
#define DHTTYPE DHT22
#define TRIG_PIN 2
#define ECHO_PIN 4
#define POT_PIN 17

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Ensure this matches your Flask computer's IP exactly
String serverName = "https://192.168.29.253:5000/";

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
}

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  // Calculate distance in cm
  return duration * 0.034 / 2;
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float d = readDistance();
    int p = analogRead(POT_PIN);

    // Force values if sensors are NaN in the simulation
    if (isnan(h)) h = 45.0;
    if (isnan(t)) t = 24.0;

    // Create the "Clean" string: "temp;hum;dist;pot"
    // No "sensor" word, no "data" word. Just numbers and semicolons.
    String dataBundle = String(t, 1) + ";" + String(h, 1) + ";" + String(d, 1) + ";" + String(p);
    
    // The final URL: https://192.168.29.253:5000/24.0;45.0;15.2;512
    String fullUrl = "https://192.168.29.253:5000/" + dataBundle;

    Serial.println("--- GHOST TRANSMISSION ---");
    Serial.println("URL: " + fullUrl);

    WiFiClientSecure *client = new WiFiClientSecure;
    client->setInsecure();
    HTTPClient http;

    http.begin(*client, fullUrl);
    int httpCode = http.GET(); 

    if (httpCode > 0) {
      Serial.printf("Server Ack: %d\n", httpCode);
    }
    
    http.end();
    delete client;
  }
  delay(5000);
}