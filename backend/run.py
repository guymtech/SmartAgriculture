#from flask import Flask

#app = Flask(__name__)

from app import create_app

app = create_app()

'''
# This catches everything after the / 
@app.route("/<path:bundle>")
def catch_all(bundle):
    print("\n" + "👻 " * 10)
    print(f"GHOST BUNDLE DETECTED: {bundle}")
    
    # If the bundle is just the word "sensor", we know it's the old code
    if bundle == "sensor":
        print("⚠️  Received old 'sensor' path. Please refresh Wokwi code.")
        return "Old code detected", 200

    try:
        # Split by the semicolon
        parts = bundle.split(';')
        
        if len(parts) >= 4:
            temp, hum, dist, pot = parts[0], parts[1], parts[2], parts[3]
            print(f"📊 DATA DECODED!")
            print(f"🌡️  Temp: {temp}°C | 💧 Hum: {hum}%")
            print(f"📏 Dist: {dist}cm | 🎡 Pot: {pot}")
            print("👻 " * 10)
            return f"Success: {bundle}", 200
        else:
            print(f"⚠️  Partial data received: {parts}")
            return "Incomplete Data", 200
            
    except Exception as e:
        print(f"❌ Decode Error: {e}")
        return "Error", 500
'''

if __name__ == "__main__":
    # Ensure adhoc SSL is still running
    app.run(host="0.0.0.0", port=5500, ssl_context='adhoc',debug=True)