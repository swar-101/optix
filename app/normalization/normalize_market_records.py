
def normalize_market_records(raw, contracts):
    fetched = raw["data"]["fetched"]

    contract_lookup = {}

    for _, row in contracts.iterrows():
        contract_lookup[str(row["token"])] = row


    normalized = []

    for item in fetched:
        contract = contract_lookup.get(item["symbolToken"])
        symbol = item["tradingSymbol"]

        option_type = (
            "CE"
            if symbol.endswith("CE")
            else "PE"
        )

        normalized.append({
            "symbol": item["tradingSymbol"],
            "token": item["symbolToken"],
            "ltp": item["ltp"],
            "oi": item["opnInterest"],
            "volume": item["tradeVolume"],
            "strike": contract["strike"],
            "option_type": option_type,
        })

    return normalized