import requests
import firebase_admin
from firebase_admin import credentials, db
import os
import json
from datetime import datetime
import pytz

def fetch_and_update():
    try:
        tz = pytz.timezone('Asia/Yangon')
        now = datetime.now(tz)
        current_time = now.hour * 100 + now.minute
        day_name = now.strftime('%a').lower() # mon, tue, wed...
        day = now.weekday()

        if day < 5:
            service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
            cred = credentials.Certificate(service_account_info)
            
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://myanmar2d3d-app-default-rtdb.firebaseio.com'
                })
            
            url = "https://api.thaistock2d.com/live"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            live_data = data.get('live')
            results = data.get('result', [])

            if 930 <= current_time <= 1201:
                if live_data:
                    db.reference('thaistock/live_results').set(live_data)
                
                if current_time >= 1158:
                    for res in results:
                        if res.get('open_time') == "12:01:00":
                            db.reference('thaistock/result_12').set(res)
                            db.reference(f'history/this_week/{day_name}/result_12').set(res.get('twod'))

            elif 1400 <= current_time <= 1631:
                if live_data:
                    db.reference('thaistock/live_results').set(live_data)
                
                if current_time >= 1628:
                    for res in results:
                        if res.get('open_time') == "16:30:00":
                            db.reference('thaistock/result_43').set(res)
                            db.reference(f'history/this_week/{day_name}/result_43').set(res.get('twod'))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
