import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime

# Firebase Secret ကို GitHub မှ ယူခြင်း
service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_and_update():
    try:
        # API မှ data ယူခြင်း
        url = "https://api.thaistock2d.com/live"
        response = requests.get(url)
        data = response.json()

        # ၁။ Live Card အတွက် (2D, Time, Set, Value)
        if 'live' in data:
            live_payload = {
                "twod": data['live'].get('twod'),
                "time": data['live'].get('time'),
                "set": data['live'].get('set'),
                "value": data['live'].get('value'),
                "date": data['live'].get('date')
            }
            db.collection('thaistock').document('live_results').set(live_payload)
            print("Live Card updated.")

        # ၂။ ၁၂:၀၁/၀၄:၃၀ Card များနှင့် မှတ်တမ်းအတွက်
        if 'result' in data:
            results = data['result']
            
            # (A) thaistock/history ထဲသို့ all_results array သိမ်းခြင်း
            db.collection('thaistock').document('history').set({"all_results": results})
            
            # (B) တစ်ပတ်စာမှတ်တမ်း (history/this_week) အတွက် ပြင်ဆင်ခြင်း
            weekly_data = {}
            days_map = {0: 'sun', 1: 'mon', 2: 'tue', 3: 'wed', 4: 'thu', 5: 'fri', 6: 'sat'}
            
            for res in results:
                stock_date = res.get('stock_date')
                open_time = res.get('open_time')
                twod_val = res.get('twod')
                
                # နေ့အမည်ကို ရှာခြင်း
                date_obj = datetime.strptime(stock_date, '%Y-%m-%d')
                day_name = days_map[date_obj.weekday() + 1 if date_obj.weekday() < 6 else 0]
                
                # ၁၂:၀၁ နှင့် ၀၄:၃၀ ခွဲခြားသိမ်းဆည်းခြင်း
                if open_time == "12:01:00":
                    weekly_data[f"{day_name}_12"] = twod_val
                elif open_time == "16:30:00":
                    weekly_data[f"{day_name}_43"] = twod_val
            
            # history/this_week သို့ ပို့ခြင်း
            if weekly_data:
                db.collection('history').document('this_week').set(weekly_data, merge=True)
                print("Weekly history updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update()
