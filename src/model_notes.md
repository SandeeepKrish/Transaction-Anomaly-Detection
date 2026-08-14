# Model Notes

Isolation Forest is an unsupervised anomaly-detection algorithm. It isolates unusual observations by recursively partitioning the feature space. It is useful for portfolio demonstrations because labeled fraud/anomaly data is often unavailable.

Features used:
- amount
- transaction hour
- day of week
- log-transformed amount

For a production system, validate the alert threshold with domain experts and labeled historical cases rather than treating every model flag as fraud.
