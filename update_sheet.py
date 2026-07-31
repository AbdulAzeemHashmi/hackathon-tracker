import requests
import os

def update_google_sheet(events):
    """
    Sends the list of events to the Google Apps Script Web App via POST.
    Requires environment variables:
      WEB_APP_URL – the deployment URL
      WEB_APP_TOKEN – a secret token you set in the Apps Script
    """
    web_app_url = os.getenv("WEB_APP_URL")
    token = os.getenv("WEB_APP_TOKEN")

    if not web_app_url or not token:
        print("❌ Missing WEB_APP_URL or WEB_APP_TOKEN in environment.")
        return

    # The Apps Script expects a JSON payload with 'token' and 'data'
    payload = {
        "token": token,
        "data": events
    }

    try:
        response = requests.post(web_app_url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ Google Sheet updated: {result.get('count')} rows added.")
            else:
                print(f"❌ Apps Script error: {result.get('error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception while updating sheet: {e}")