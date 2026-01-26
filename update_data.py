import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def fetch_and_update():
    try:
        service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
        cred = credentials.Certificate(service_account_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        url = "https://api.thaistock2d.com/live"
        data = requests.get(url, timeout=5).json()

        if 'live' in data:
            db.collection('thaistock').document('live_results').set(data['live'])

        if 'result' in data:
            for res in data['result']:
                if res.get('open_time') == "12:01:00":
                    db.collection('thaistock').document('result_12').set(res)
                elif res.get('open_time') == "16:30:00":
                    db.collection('thaistock').document('result_43').set(res)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
