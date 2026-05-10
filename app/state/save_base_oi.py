def save_base_oi(base_oi):
    path = _base_oi_path()
    try:
        serialisable = {
            key: df[['strike', 'CE_OI', 'PE_OI']].to_dict(orient='records')
            for key, df in base_oi.items()
        }
        with open(path, 'w') as f:
            json.dump(serialisable, f)
    except Exception as e:
        print(f"⚠️  Could not save base OI ({path}): {e}")