# MarketFabric

MarketFabric is a modular market-data runtime designed to offload options-chain ingestion, normalization, and analytics from Excel-based trading workflows.
The system focuses on reliable observational decision support for options monitoring workflows.

## Why MarketFabric Exists

The project was created to improve the responsiveness, stability, and reliability of Excel-driven market observation systems used for options analysis.

Instead of tightly coupling market computation directly to Excel runtime behavior, MarketFabric separates:

- ingestion
- normalization
- computation
- presentation

This allows Excel to behave as a lightweight observational client rather than the primary execution engine.

---

## Current Scope (V1)

MarketFabric V1 currently focuses on:

- AngelOne SmartAPI integration
- live option-chain ingestion
- normalized option records
- CE/PE strike pairing
- Open Interest (OI) change tracking
- CSV-based output generation
- runtime stabilization and architecture extraction

See the full V1 scope here:

-> [V1 Specification](docs/market-fabric-v1.md)

---

## Architecture
Current runtime flow:

```text
Broker API
    ↓
Authentication
    ↓
Scrip Master Resolution
    ↓
Token Resolution
    ↓
Market Data Fetch
    ↓
Normalization
    ↓
State Management
    ↓
Analytics
    ↓
Output Adapters
```

### Components

* Ingestion Layer
  Fetches option chain data from broker API

* State Manager
  Maintains previous values (OI, IV, price)

* Compute Engine

  * IV estimation (iterative solver)
  * Greeks computation
  * OI change calculation

* Output Layer
  Writes structured data to CSV

---

## Project Structure

```text
market-fabric/
│
├── app/
│   ├── auth/
│   ├── metadata/
│   ├── ingestion/
│   ├── normalization/
│   ├── compute/
│   ├── state/
│   ├── output/
│   └── utils/
│
├── data/
├── docs/
├── logs/
└── run.py
```

---

## Installation

```
pip install -r requirements.txt
```

---

## Running

### Demo Mode

```bash
python run.py --mode demo
```

### Live Mode

```bash
python run.py --mode live
```

Requires valid API credentials in `.env`.

---

## Configuration

Edit `config.py`:

* Symbols (e.g., NIFTY, BANKNIFTY)
* Strike range
* Expiry
* Refresh interval

---

## Output Schema

CSV columns:

* symbol
* strike
* option_type (CE/PE)
* ltp
* oi
* change_oi
* iv
* delta
* gamma
* vega
* theta

---

## Performance Strategy

* Reuse previous IV as initial guess
* Skip recomputation for small price changes
* O(1) state lookups via dictionary
* Batch processing per tick

---

## Notes

* Greeks are model-dependent and may vary slightly across platforms
* IV is computed numerically and may introduce approximation error
* Designed for decision support, not exact replication of exchange/vendor data

---

## Future Improvements

* Direct Excel integration
* Web dashboard
* Alert system for OI/IV anomalies
* Parallel computation

---