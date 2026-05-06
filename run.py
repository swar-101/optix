"""CLI entry point for MarketFabric (demo/live mode)."""

import argparse
from app.main import run


def main():
    parser = argparse.ArgumentParser(description="MarketFabric - Real-time options analytics engine")
    parser.add_argument(
        "--mode",
        choices=["demo", "live"],
        required=True,
        help="Run mode: 'demo' uses mock data, 'live' connects to broker API",
    )
    args = parser.parse_args()
    run(mode=args.mode)


if __name__ == "__main__":
    main()
