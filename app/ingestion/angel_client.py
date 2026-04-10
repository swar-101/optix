"""AngelOne broker API integration."""

import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_BASE_URL = "https://apiconnect.angelbroking.com"


class AngelClient:
    """Thin wrapper around the AngelOne SmartAPI."""

    def __init__(self):
        self.api_key = os.getenv("API_KEY", "")
        self.api_secret = os.getenv("API_SECRET", "")
        self.client_id = os.getenv("CLIENT_ID", "")
        self._token: str = ""

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def login(self) -> None:
        url = f"{_BASE_URL}/rest/auth/angelbroking/user/v1/loginByPassword"
        payload = {
            "clientcode": self.client_id,
            "password": self.api_secret,
        }
        headers = {
            "Content-Type": "application/json",
            "X-UserType": "USER",
            "X-SourceID": "WEB",
            "X-ClientLocalIP": "127.0.0.1",
            "X-ClientPublicIP": "127.0.0.1",
            "X-MACAddress": "00:00:00:00:00:00",
            "X-PrivateKey": self.api_key,
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        self._token = response.json()["data"]["jwtToken"]
        logger.info("AngelClient authenticated successfully")

    # ------------------------------------------------------------------
    # Data fetch
    # ------------------------------------------------------------------

    def fetch_option_chain(self, symbols: list[str]) -> list[dict]:
        """Return raw option chain records for *symbols*."""
        if not self._token:
            self.login()
        records: list[dict] = []
        for symbol in symbols:
            logger.debug("Fetching option chain for %s", symbol)
            # TODO: implement actual endpoint call and parse response
            records.extend(self._fetch_symbol(symbol))
        return records

    def _fetch_symbol(self, symbol: str) -> list[dict]:
        """Fetch and parse option chain for a single symbol."""
        # Placeholder — replace with real endpoint and parsing logic
        return []
