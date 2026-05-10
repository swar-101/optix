"""AngelOne broker API integration."""
import json
import os
import logging
from dotenv import load_dotenv

from app.auth.get_angel_one_session import get_angel_one_session
from app.ingestion.fetch_market_data import fetch_market_data
from app.metadata.get_scrip_master import get_scrip_master
from app.metadata.resolve_contracts import resolve_contracts
from app.normalization.normalize_market_records import normalize_market_records

load_dotenv()
logger = logging.getLogger(__name__)

# _BASE_URL = "https://apiconnect.angelbroking.com"


class AngelClient:
    """Thin wrapper around the AngelOne SmartAPI."""

    def __init__(self):
        self.api_key = os.getenv("API_KEY", "P789668")
        self.api_secret = os.getenv("API_SECRET", "1713")
        self.client_id = os.getenv("CLIENT_ID", "P789668")
        self.master = get_scrip_master()

        with open('AngelOne_config.json') as f:
            config = json.load(f)
            self.config = config

        self.client = get_angel_one_session(self.config)

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------



    # ------------------------------------------------------------------
    # Data fetch
    # ------------------------------------------------------------------

    def fetch_option_chain(self, symbols: list[str]) -> list[dict]:
        """Return raw option chain records for *symbols*."""

        records: list[dict] = []
        for symbol in symbols:
            logger.debug("Fetching option chain for %s", symbol)
            # TODO: implement actual endpoint call and parse response
            records.extend(self._fetch_symbol(symbol))
        return records

    def _fetch_symbol(self, symbol: str):
        """Fetch and parse option chain for a single symbol."""
        contracts = resolve_contracts(self.master, symbol)
        if contracts.empty:
            print("No contracts resolved.")
            return []

        subset = contracts.head(10)

        tokens = subset["token"].astype(str).tolist()
        if not tokens:
            print("No tokens extracted.")
            return []

        print(contracts[[
            "token",
            "symbol",
            "expiry",
            "strike"
        ]].head())

        raw = fetch_market_data(
            client=self.client,
            exchange="NFO",
            tokens=tokens
        )
        if not raw.get("status"):
            print(raw)
            return []

        normalized = normalize_market_records(raw, contracts)

        print(normalized)

        return normalized