# Optix

Real-time options analytics engine for computing Implied Volatility (IV), Greeks, and Open Interest (OI) changes from live market data.

## Overview

Optix is a stateful computation engine that ingests live options data, processes it efficiently, and outputs structured analytics for downstream consumption (Excel, CSV, dashboards).

The system is designed for low-latency updates, minimal recomputation, and decision-grade accuracy.

---

## Features

* Real-time option chain ingestion
* Change in Open Interest (OI) computation
* Implied Volatility (IV) solver
* Greeks computation (Delta, Gamma, Vega, Theta)
* Stateful caching for performance optimization
* CSV output compatible with Excel dashboards
* Demo mode with mock data

---

## Architecture

Data Flow:

Data Source → Ingestion → State Manager → Compute Engine → Output Writer

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

## Folder Structure

```
optix/
│
├── app/
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration (symbols, refresh rate)
│
│   ├── ingestion/
│   │   └── angel_client.py    # API integration
│
│   ├── state/
│   │   └── state_manager.py   # Stores previous OI, IV, prices
│
│   ├── compute/
│   │   ├── iv_solver.py       # Implied Volatility solver
│   │   ├── greeks.py          # Greeks calculations
│   │   └── oi.py              # OI change logic
│
│   ├── output/
│   │   └── writer.py          # CSV writer
│
│   ├── utils/
│   │   └── time_utils.py
│
│   └── demo/
│       └── mock_data.py       # Demo mode generator
│
├── data/
│   └── output.csv             # Generated output
│
├── logs/
│   └── app.log
│
├── .env                       # API credentials
├── requirements.txt
├── README.md
└── run.py                     # CLI entry (demo/live)
```

---

## Installation

```
pip install -r requirements.txt
```

---

## Running

### Demo Mode

```
python run.py --mode demo
```

Generates mock data and writes to CSV.

---

### Live Mode

```
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