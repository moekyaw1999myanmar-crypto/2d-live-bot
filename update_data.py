import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime
import pytz

def fetch_and_update():
    try:
        tz = pytz.timezone('Asia/Yangon')
        now = datetime.now(tz)
        current_time = now.hour * 100 + now.minute
        day = now.weekday()

        if day < 5:
            is_valid_time = (930 <= current_time <= 1205) or (1400 <= current_time <= 1645)
            
            if is_valid_time:
                if not firebase_admin._apps:
                    service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
                    cred = credentials.Certificate(service_account_info)
                    firebase_admin.initialize_app(cred)
                
                db = firestore.client()

                url = "https://api.thaistock2d.com/live"
                response = requests.get(url, timeout=10)
                data = response.json()

                if 'live' in data and data['live'].get('twod') != "--":
                    db.collection('thaistock').document('live_results').set(data['live'], merge=True)

                if 'result' in data:
                    for res in data['result']:
                        if res.get('twod') and res.get('twod') != "--":
                            if res.get('open_time') == "12:01:00":
                                db.collection('thaistock').document('result_12').set(res, merge=True)
                            elif res.get('open_time') == "16:30:00":
                                db.collection('thaistock').document('result_43').set(res, merge=True)
                                
    except Exception:
        pass

if __name__ == "__main__":
    fetch_and_update()
