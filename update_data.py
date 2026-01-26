import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime
import pytz

def fetch_and_update():
    try:
        # မြန်မာစံတော်ချိန် (GMT+6:30) သတ်မှတ်ခြင်း
        tz = pytz.timezone('Asia/Yangon')
        now = datetime.now(tz)
        current_time = now.hour * 100 + now.minute
        day = now.weekday() # 0 = Monday, 6 = Sunday

        # စနေ၊ တနင်္ဂနွေ မဟုတ်မှသာ အလုပ်လုပ်မည်
        if day < 5:
            # မနက် (9:30 - 12:01) သို့မဟုတ် ညနေ (14:00 - 16:30)
            is_live_time = (930 <= current_time <= 1201) or (1400 <= current_time <= 1630)
            
            if is_live_time:
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
                print(f"Synced at {now.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
