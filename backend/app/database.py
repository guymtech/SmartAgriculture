import os
import firebase_admin
from firebase_admin import credentials, db

class FirebaseDatabase:
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            # This finds the 'backend' folder path automatically
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cert_path = os.path.join(base_dir, "serviceAccountKey.json")
            
            if not os.path.exists(cert_path):
                raise FileNotFoundError(f"❌ Critical: {cert_path} not found!")

            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://fir-91b5c-default-rtdb.firebaseio.com/'
            })
            cls._initialized = True
            print("🔥 Firebase Initialized Successfully")
            
    @staticmethod
    def store_sensor_data(temp, hum, dist, pot, decision):
        """Stores a new entry under the 'sensor_logs' node"""
        try:
            ref = db.reference('sensor_logs')
            new_data_ref = ref.push({
                'temperature': temp,
                'humidity': hum,
                'distance': dist,
                'potentiometer': pot,
                'irrigation_command': decision,
                'timestamp': {".sv": "timestamp"} # Firebase Server Timestamp
            })
            return new_data_ref.key
        except Exception as e:
            print(f"❌ Firebase Error: {e}")
            return None
        
    @staticmethod
    def get_sensor_logs(limit=50):
        """Fetch latest sensor logs without requiring Firebase indexes"""
        try:
            ref = db.reference("sensor_logs")
            data = ref.get()

            if not data:
                return []

            # convert dict -> list
            logs = list(data.values())

            # sort locally instead of Firebase query
            logs.sort(key=lambda x: x.get("timestamp", 0))

            # return last N entries
            return logs[-limit:]

        except Exception as e:
            print(f"❌ Fetch Error: {e}")
            return []