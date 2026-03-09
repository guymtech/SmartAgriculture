#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <DHT.h>
#include <ESP32Servo.h>

// Pin Definitions based on your diagram.json
#define DHTPIN 15
#define DHTTYPE DHT22
#define TRIG_PIN 2
#define ECHO_PIN 4
#define POT_PIN 34    // Matches your updated diagram.json
#define SERVO_PIN 5
#define BUZZER_PIN 19

DHT dht(DHTPIN, DHTTYPE);
Servo irrigationServo;

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Actuator Setup
  irrigationServo.attach(SERVO_PIN);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Sensor Setup
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // WiFi Connection
  Serial.print("Connecting to WiFi");
  WiFi.begin("Wokwi-GUEST", "");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
}

float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2;
}

int servoPos = 0;       // Current position
int servoStep = 5;      // How many degrees to move per update
unsigned long lastServoMove = 0; 
int servoInterval = 50; // Speed of movement (lower is faster)
bool isIrrigating = false; // Track server command

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // 1. Read Sensors (Directly into variables)
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float d = getDistance();
    int p = analogRead(POT_PIN);

    // 2. Safety: Handle DHT22 "NaN" errors
    if (isnan(h)) h = 0.0;
    if (isnan(t)) t = 0.0;

    // 3. Serial Debug (Watch this in VS Code to see if sliders work)
    Serial.printf("READING -> T:%.1f H:%.1f D:%.1f P:%d\n", t, h, d, p);

    // 4. Build Ghost Bundle (Added @ marker for your Flask filter)
    String bundle = "@" + String(t, 1) + ";" + String(h, 1) + ";" + String(d, 1) + ";" + String(p);
    
    // Ensure Port 5500 matches your Flask run.py
    String fullUrl = "https://10.57.127.12:5500/" + bundle;

    WiFiClientSecure *client = new WiFiClientSecure;
    client->setInsecure(); // Needed for 'adhoc' SSL
    HTTPClient http;

    http.begin(*client, fullUrl);
    int httpCode = http.GET();

    if (httpCode == 200) {
      String response = http.getString();
      response.trim(); 
      Serial.println("Server Command Received: [" + response + "]");

      // 5. Parse "SERVO|BUZZER" (Expected format "1|0")
      if (response.length() >= 3) {
        char servoCmd = response.charAt(0);
        char buzzCmd  = response.charAt(2);

        // Actuate Servo
        isIrrigating = (servoCmd == '1');

        // Actuate Buzzer
        if (buzzCmd == '1') digitalWrite(BUZZER_PIN, HIGH);
        else digitalWrite(BUZZER_PIN, LOW);
      }
    } else {
      Serial.print("HTTP Error: ");
      Serial.println(httpCode);
    }
    if (isIrrigating) {
    if (millis() - lastServoMove >= servoInterval) {
      lastServoMove = millis();
      
      servoPos += servoStep;

      // Sweep logic: if it hits 180 or 0, reverse direction
      if (servoPos >= 180 || servoPos <= 0) {
        servoStep = -servoStep; 
      }
      
      irrigationServo.write(servoPos);
      Serial.print("Servo Swiping: "); Serial.println(servoPos);
    }
  } else {
    // If irrigation is OFF, return to 0 slowly or snap to 0
    if (servoPos != 0) {
      servoPos = 0;
      irrigationServo.write(servoPos);
      Serial.println(">> Irrigation: OFF (Resetting to 0)");
    }
  }
    
    http.end();
    delete client;
  }
  
  delay(20000); // 4-second interval is best for DHT stability
}