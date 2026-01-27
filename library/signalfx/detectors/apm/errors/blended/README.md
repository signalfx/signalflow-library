Detect when the error rate exceeds recent empirical baselines.

## Detector

The `blended` function detects when the error rate exceeds the observed error rate over the last 12h, the same time yesterday, and the same time 1 week ago.

Parameters:
- `guard: float = 300.0` sets a floor for the alert trigger threshold.
- `headroom: float = 1.5`, typically between 1 and 2, raises the alert trigger threshold - lower is more sensitive.

It returns a detect block that fires when error rate has degraded beyond observed norms for 80% of the last 15 minutes.


#### Example usage
```
from signalfx.detectors.apm.errors.blended import blended

blended.blended(guard=30, headroom=1.0).publish('my-error-detector')
```

