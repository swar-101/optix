def fetch_market_data(client, exchange, tokens):
    response = client.getMarketData(
        mode="FULL",
        exchangeTokens={
            exchange: tokens
        }
    )

    return response