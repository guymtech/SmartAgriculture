# app/services.py

class IrrigationService:
    @staticmethod
    def evaluate_conditions(temp, hum, dist):
        """
        MTech Logic: 
        1. Irrigation (Servo) triggers if Humidity is low AND Temp is high.
        2. Alert (Buzzer) triggers if Distance is too low (Obstacle/Tank empty).
        """
        # Thresholds
        TEMP_THRESHOLD = 30.0
        HUM_THRESHOLD = 20.0
        DIST_THRESHOLD = 50.0

        irrigation_on = False
        alert_on = False

        # Logic for Servo (Irrigation)
        if hum < HUM_THRESHOLD and temp > TEMP_THRESHOLD:
            irrigation_on = True

        # Logic for Buzzer (Alert)
        if dist < DIST_THRESHOLD:
            alert_on = True

        # Return a simple command string for the ESP32
        # Format: "SERVO_STATE|BUZZER_STATE"
        cmd_servo = "1" if irrigation_on else "0"
        cmd_buzz  = "1" if alert_on else "0"
        
        return f"{cmd_servo}|{cmd_buzz}"