⚠️ Deprecation warning: superceded by the autodetect.apm.errors.blended function.

Detect when the error rate or error percentage exceeds recent empirical baselines.

## `blended` — error rate detector

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

## `blended_percent` — error percentage detector

The `blended_percent` function detects when the error percentage (errors / total requests) exceeds observed norms over the last 12h, the same time yesterday, and the same time 1 week ago.

| Parameter name | Type     | Description | Default value |
|:---------------|:---------|:------------|:--------------|
| guard          | float    | Floor for the alert trigger threshold (in percent) | 1.0 |
| headroom       | float    | Multiplier applied to the historical baseline to set the trigger threshold; lower is more sensitive | 1.5 |
| window         | duration | Aggregation window for computing the error percentage | duration('5m') |
| min_requests   | int      | Minimum number of total requests in the aggregation window required before an alert can fire | 10 |
| filter_        | filter   | Optionally refine the set of observed entities | None |
| resource_type  | string   | Key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow); use `'service'` for service-level monitoring (`service.request` metric) or `'service_operation'` for endpoint monitoring (`spans` metric) | `'service'` |

It returns a detect block that fires when the error percentage has degraded beyond observed norms for 80% of the last 15 minutes, provided at least `min_requests` requests were made in the aggregation window.


#### Example usage
```
from signalfx.detectors.apm.errors.blended import blended_percent

# Service-level monitoring (default)
blended_percent.blended_percent(guard=1.0, headroom=1.5).publish('my-error-pct-detector')

# Endpoint monitoring using spans metric
blended_percent.blended_percent(
    resource_type='service_operation',
    filter_=filter('sf_service', 'my_svc') and filter('sf_operation', 'my_op'),
).publish('my-endpoint-error-pct-detector')
```

