import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_and_update():
    try:
        url = "https://api.thaistock2d.com/live"
        response = requests.get(url)
        data = response.json()

        if 'live' in data:
            live_data = {
                "twod": data['live'].get('twod'),
                "time": data['live'].get('time'),
                "set": data['live'].get('set'),
                "value": data['live'].get('value')
            }
            db.collection('thaistock').document('live_results').set(live_data)

        if 'result' in data:
            results = data['result']
            for res in results:
                card_data = {
                    "twod": res.get('twod'),
                    "set": res.get('set'),
                    "value": res.get('value')
                }
                
                if res.get('open_time') == "12:01:00":
                    db.collection('thaistock').document('result_12').set(card_data)
                
                elif res.get('open_time') == "16:30:00":
                    db.collection('thaistock').document('result_43').set(card_data)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
            for res in results:
                card_data = {
                    "twod": res.get('twod'),
                    "set": res.get('set'),
                    "value": res.get('value')
                }
                
                if res.get('open_time') == "12:01:00":
                    db.collection('thaistock').document('result_12').set(card_data)
                    print("12:01 Card updated.")
                
                elif res.get('open_time') == "16:30:00":
                    db.collection('thaistock').document('result_43').set(card_data)
                    print("16:30 Card updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
