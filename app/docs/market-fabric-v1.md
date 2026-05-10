# MarketFabric V1 Specification

## Objective

MarketFabric V1 aims to provide a stable and modular runtime for ingesting and processing options-chain market data for observational decision support workflows.

The primary target presentation layer is Excel.

---

# V1 Goals

## Core Runtime

- establish stable broker authentication
- fetch live options-chain data
- normalize market records
- pair CE/PE contracts by strike
- compute OI change
- maintain lightweight runtime state
- generate structured CSV outputs

---

# V1 User Workflow

The runtime is designed for users who:

- monitor options chains observationally
- compare CE vs PE activity
- track OI movement
- observe premium movement
- use Excel dashboards for decision support

The runtime is NOT intended for:

- high-frequency trading
- automated execution
- predictive AI systems
- low-latency trading infrastructure

---

# Canonical Runtime Principle

MarketFabric establishes a single canonical runtime truth.

Presentation layers such as:

- CLI
- CSV
- Excel
- future dashboards

should consume the same normalized runtime observations.

Presentation layers should not independently compute analytics.

---

# Current Runtime Pipeline

```text
Broker API
    ↓
Authentication
    ↓
Scrip Master
    ↓
Token Resolution
    ↓
Market Fetch
    ↓
Normalization
    ↓
State Tracking
    ↓
Computation
    ↓
Output Projection
```

---

# Current Supported Broker

- AngelOne SmartAPI

---

# Current Supported Instrument

- NIFTY options

---

# Current Runtime Behavior

- polling-based ingestion
- configurable refresh interval
- configurable ATM-focused strike monitoring
- long-running polling runtime during market sessions
- normalized runtime records
- stateful OI tracking
- CSV projection generation

---

# Explicit Non-Goals (V1)

The following are intentionally deferred:

- websocket streaming
- multi-broker abstraction
- cloud deployment
- distributed systems
- retries/backoff optimization
- advanced caching
- alert engines
- execution systems
- predictive AI models
- portfolio management

---

# Engineering Priorities

Priority order:

1. ingestion correctness
2. normalization stability
3. runtime observability
4. presentation consistency
5. modular responsibility separation
6. performance optimization

---

# Success Criteria

V1 is considered successful if:

- live market data ingestion remains stable
- normalized records are reliable
- CE/PE pairing is correct
- OI changes are accurately tracked
- Excel-compatible outputs remain usable
- runtime responsibilities remain modular