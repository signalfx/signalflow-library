⚠️ Deprecation warning: superceded by the autodetect.apm.latency.blended function.

Detect when the p90 latency exceeds recent empirical baselines.

## Detector

The `blended` function detects when the p90 latency exceeds the observed p90 latency over the last 12h, the same time yesterday, and the same time 1 week ago.

Parameters:
- `guard: float = 250.0` (millis) sets a floor for the alert trigger threshold.
- `headroom: float = 1.5`, typically between 1 and 2, raises the alert trigger threshold - lower is more sensitive.

It returns a detect block that fires when p90 latency has degraded beyond observed norms for 80% of the last 15 minutes.


#### Example usage
```
from signalfx.detectors.apm.latency.blended import blended

blended.blended(guard=100, headroom=1.0).publish('my-latency-detector')
```

