from flask import Blueprint, request
from .services import IrrigationService
from .database import FirebaseDatabase

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