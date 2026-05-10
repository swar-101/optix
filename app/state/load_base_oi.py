def load_base_oi():
    path = _base_oi_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as f:
            raw = json.load(f)
        result = {}
        for key, records in raw.items():
            df = pd.DataFrame(records)
            df['strike'] = df['strike'].astype(float)
            df['CE_OI']  = df['CE_OI'].astype(float)
            df['PE_OI']  = df['PE_OI'].astype(float)
            result[key] = df
        print(f"📂 Loaded baseline OI from {path}  ({len(result)} sheet(s))")
        return result
    except Exception as e:
        print(f"⚠️  Could not load base OI file ({path}): {e}")
        return {}