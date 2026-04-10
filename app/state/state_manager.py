"""State manager — stores previous OI, IV, and prices."""

import logging

logger = logging.getLogger(__name__)


class StateManager:
    """In-memory store for per-contract state across ticks."""

    def __init__(self):
        # key: (symbol, strike, option_type) → dict with oi, iv, ltp
        self._store: dict[tuple, dict] = {}

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get(self, symbol: str, strike: float, option_type: str) -> dict | None:
        """Return previous state for the given contract, or *None*."""
        return self._store.get((symbol, strike, option_type))

    def get_oi(self, symbol: str, strike: float, option_type: str) -> float:
        """Return previous OI for the contract, or 0 if unseen."""
        record = self.get(symbol, strike, option_type)
        return record["oi"] if record else 0.0

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def update(self, option: dict) -> None:
        """Persist the latest snapshot for a contract."""
        key = (option["symbol"], option["strike"], option["option_type"])
        self._store[key] = {
            "oi": option.get("oi", 0.0),
            "iv": option.get("iv", 0.0),
            "ltp": option.get("ltp", 0.0),
        }
        logger.debug("State updated for %s", key)
