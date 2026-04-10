"""CSV writer for structured analytics output."""

import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_OUTPUT_PATH = Path(__file__).resolve().parents[2] / "data" / "output.csv"

_FIELDS = [
    "symbol",
    "strike",
    "option_type",
    "ltp",
    "oi",
    "change_oi",
    "iv",
    "delta",
    "gamma",
    "vega",
    "theta",
]


def write_csv(records: list[dict], path: Path = _OUTPUT_PATH) -> None:
    """Write *records* to a CSV file, overwriting any existing content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    logger.info("Output written to %s (%d rows)", path, len(records))
