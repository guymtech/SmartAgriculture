from flask import Blueprint, request
from .services import IrrigationService
from .database import FirebaseDatabase
from flask import jsonify
from flask import render_template

main_bp = Blueprint('main', __name__)

# Initialize Firebase once when the blueprint is loaded
FirebaseDatabase.initialize()

@main_bp.route("/<path:bundle>")
def handle_iot_data(bundle):
    if bundle.startswith("@"):
        clean_bundle = bundle[1:]
    else:
        return "Ignore", 200
    
    try:
        parts = clean_bundle.split(';')
        if len(parts) >= 4:
            t, h, d, p = map(float, parts)
            
            # 1. Get the decision (Logic Layer)
            command = IrrigationService.evaluate_conditions(t, h, d)
            
            # 2. Store in Firebase (Database Layer)
            FirebaseDatabase.store_sensor_data(t, h, d, p, command)
            
            print(f"📊 Data Saved to Firebase | CMD: {command}")
            return command, 200
            
    except Exception as e:
        print(f"❌ Route Error: {e}")
        return "0|0", 400

@main_bp.route("/api/sensor-data")
def get_sensor_data():
    data = FirebaseDatabase.get_sensor_logs()

    if not data:
        return jsonify([])

    result = []

    for value in data:
        result.append({
            "temperature": value.get("temperature"),
            "humidity": value.get("humidity"),
            "distance": value.get("distance"),
            "potentiometer": value.get("potentiometer"),
            "command": value.get("irrigation_command"),
            "timestamp": value.get("timestamp")
        })

    return jsonify(result)

@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")