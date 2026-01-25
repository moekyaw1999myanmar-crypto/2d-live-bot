import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Firebase Secret ကို GitHub မှ ယူခြင်း
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

        # Firestore ထဲသို့ Data ထည့်ခြင်း
        if 'live' in data:
            db.collection('thaistock').document('live_results').set(data['live'])
            print("Live data updated.")
        
        if 'result' in data:
            db.collection('thaistock').document('history').set({"all_results": data['result']})
            print("History updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
