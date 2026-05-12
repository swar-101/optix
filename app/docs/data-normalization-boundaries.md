
* canonical data
* contextual data
* noise candidates
* future evolution notes


| Field  | Candidate Type   | Why                             |
| ------ | ---------------- | ------------------------------- |
| token  | canonical        | stable instrument identity      |
| symbol | canonical        | reused lookup entity            |
| expiry | canonical        | query/filter critical           |
| strike | canonical        | analytics + joins               |
| ltp    | contextual       | rapidly changing market state   |
| oi     | contextual       | temporal market observation     |
| volume | contextual       | historical/time-series oriented |
| logs   | noise/contextual | operational debugging only      |


## Canonical Grouping Hypothesis

The primary analytical entity is likely:

(symbol, expiry, strike)

CE and PE contracts are treated as paired analytical projections
of the same strike-space entity rather than isolated instruments.
