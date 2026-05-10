"""Entry point for the MarketFabric computation loop."""

import logging
import time

from app.config import SYMBOLS, REFRESH_INTERVAL
from app.ingestion.angel_client import AngelClient
from app.state.state_manager import StateManager
from app.compute.iv_solver import solve_iv
from app.compute.greeks import compute_greeks
from app.compute.oi import compute_oi_change
from app.output.writer import write_csv
from app.demo.mock_data import generate_mock_chain
from app.utils.banner import print_banner

logger = logging.getLogger(__name__)


def run(mode: str = "demo") -> None:
    """Start the analytics engine in the given mode."""
    state = StateManager()
    client = None

    if mode == "live":
        client = AngelClient()
        print_banner()

    while True:

        if mode == "demo":
            chain = generate_mock_chain(SYMBOLS)

        elif mode == "live":
            logger.info("Fetching new market tick...")
            chain = client.fetch_option_chain(SYMBOLS)

        else:
            raise ValueError(f"Unknown mode: {mode}")

        results = []

        for option in chain:
            oi_change = compute_oi_change(state, option)
            iv = solve_iv(option)
            greeks = compute_greeks(option, iv)

            state.update(option)

            results.append({
                **option,
                "change_oi": oi_change,
                "iv": iv,
                **greeks
            })

        write_csv(results)

        logger.info(
            "Tick processed: %d records written",
            len(results)
        )
        
        time.sleep(REFRESH_INTERVAL)