from flask import Blueprint, request
from .services import IrrigationService
# Create the blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route("/<path:bundle>")
def handle_iot_data(bundle):
    print(f"DEBUG: Raw bundle: '{bundle}'")

    if bundle.startswith("@"):
        # Remove the @ so we have '24.0;40.0;...'
        target_data = bundle[1:] 
        print(f"🚀 [SKETCH FOLDER] Processing: {target_data}")
    else:
        print(f"⚠️ [GHOST] Ignoring: {bundle}")
        return "Ignore", 200
    
    try:
        # USE target_data instead of bundle here!
        parts = target_data.split(';')
        if len(parts) >= 4:
            t = float(parts[0])
            h = float(parts[1])
            d = float(parts[2])
            p = float(parts[3])
            
            # Decision Logic
            command = IrrigationService.evaluate_conditions(t, h, d)
            
            print(f"📊 SENSOR UPDATE | T:{t} H:{h} D:{d} | 🤖 CMD: {command}")
            return command, 200
            
        return "Invalid Format", 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return "0|0", 400
    
    
'''
def handle_ghost_data(bundle):
    # Professional logging
    print(f"\n[INCOMING] Ghost Bundle: {bundle}")
    
    if bundle == "favicon.ico":
        return "", 204

    try:
        # Split the data sent by ESP32 (temp;hum;dist;pot)
        parts = bundle.split(';')
        
        if len(parts) >= 4:
            data = {
                "temp": float(parts[0]),
                "hum":  float(parts[1]),
                "dist": float(parts[2]),
                "pot":  int(parts[3])
            }
            
            # This is where you'd eventually save to a Database
            print("="*30)
            print(f"📊 SENSOR UPDATE")
            print(f"Temperature: {data['temp']}°C")
            print(f"Humidity:    {data['hum']}%")
            print(f"Distance:    {data['dist']}cm")
            print(f"Pot Value:   {data['pot']}")
            print("="*30)
            
            return f"Data {bundle} received", 200
        
        return "Invalid Format", 400

    except Exception as e:
        print(f"Error processing bundle: {e}")
        return "Internal Error", 500
'''

@main_bp.route("/")
def index():
    return "IoT Backend Active", 200

