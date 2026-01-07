Detect when the request rate drops below empirical baselines.

## Detector

The `blended` function detects when the request rate drops below the observed request rate over the last 12h, the same time yesterday, and the same time 1 week ago.

Parameters:
- `guard: float = 600` (requests per hour) sets a floor so low-traffic services are ignored.
- `sensitivity: float = 0.85`, typically between 0.5 and 1.0, lowers the alert trigger threshold.

It returns a detect block that fires when request rate has degraded beyond observed norms for 80% of the last 15 minutes.


#### Example usage
```
from signalfx.detectors.apm.requests.blended import blended

blended.detector(guard=10, sensitivity=1.0).publish('my-request-rate-detector')
```

