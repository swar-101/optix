import json
import urllib
import pandas as pd

def get_scrip_master():
    """
    Downloads the latest scrip master from AngelOne CDN on every startup.
    Near-term weekly expiries (e.g. N1 / N4) are only added to the master
    2-3 days before expiry, so a stale local file will always miss them.
    Falls back to the local JSON file if the download fails.
    """
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    try:
        print("⬇️  Downloading fresh scrip master from AngelOne...")
        with urllib.request.urlopen(url, timeout=30) as r:
            df = pd.DataFrame(json.loads(r.read().decode()))
        df['token']  = df['token'].astype(str)
        df['expiry'] = df['expiry'].str.upper()
        print(f"✅ Scrip master downloaded: {len(df):,} instruments")
        try:
            with open("OpenAPIScripMaster.json", 'w', encoding='utf-8') as f:
                json.dump(json.loads(df.to_json(orient='records')), f)
        except Exception:
            pass
        return df
    except Exception as e:
        print(f"⚠️ Live download failed ({e}) — falling back to local file")
        with open("OpenAPIScripMaster.json", 'r', encoding='utf-8') as f:
            df = pd.DataFrame(json.load(f))
        df['token']  = df['token'].astype(str)
        df['expiry'] = df['expiry'].str.upper()
        print(f"✅ Local scrip master loaded: {len(df):,} instruments")
        return df