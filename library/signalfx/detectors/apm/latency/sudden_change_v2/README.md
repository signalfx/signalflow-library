Detect when latency exhibits a sudden increase.


## Growth rate

The `growth_rate` function detects when latency grows by a specified amount relative to the preceding window. It has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|pctile|number|percentile to monitor, one of 50, 90, 99|90|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|current_window|duration|window whose latency is evaluated for being too high|duration('5m')|
|historical_window|duration|window whose latency is used to define the baseline|duration('1h')|
|fire_growth_rate_threshold|number|latency growth required to trigger|0.2|
|clear_growth_rate_threshold|number|latency growth required to clear|0.1|
|fire_lasting|lasting|duration for which the trigger threshold must be met before the detector fires an alert|None|
|exclude_errors|boolean|whether to exclude error spans from latency metric|True|
|group_by|list of strings|average latency by these (in addition to default grouping associated with resource type)|None|
|volume_static_threshold|number|threshold on request rate (per second) required for alert to trigger|None|
|volume_relative_threshold|number|require request rate on window being evaluated to be at least this proportion of request rate on preceding window (used for trigger and clear)|None|
|vol_pctile_req_pos|number (percentage)|percentage of historical window permitted to have request rate 0|90|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|

It returns a detect block that triggers when the specified percentile of latency, suitably
filtered and grouped, over the last `current_window` is greater than
`1 + fire_growth_rate_threshold` times the latency (for the same percentile,
similarly filtered and grouped) of the preceding `historical_window`, and when volume conditions are met;
clears when latency is less than `1 + clear_growth_rate_threshold` times the baseline.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency.sudden_change_v2 import sudden_change

sudden_change.growth_rate(pctile=50, filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~


## Deviations from norm

The `deviations_from_norm` function detects when latency is too many deviations from the norm established in the preceding window. It has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|current_window|duration|window whose latency is evaluated for being too high|duration('5m')|
|historical_window|duration|window whose latency is used to define the baseline|duration('1h')|
|exclude_errors|boolean|whether to exclude error spans from latency metric|True|
|group_by|list of strings|average latency by these (in addition to default grouping associated with resource type)|None|
|fire_num_dev_threshold|number|number of historical (P90 - P50)'s from the historical P50 the current P50 must be in order to trigger|3.5|
|clear_num_dev_threshold|number|number of historical (P90 - P50)'s from the historical P50 the current P50 must be in order to clear|3|
|fire_lasting|lasting|duration for which the trigger threshold must be met before the detector fires an alert|None|
|volume_static_threshold|number|threshold on request rate (per second) required for alert to trigger|None|
|volume_relative_threshold|number|require request rate on window being evaluated to be at least this proportion of request rate on preceding window (used for trigger and clear)|None|
|fire_latency_static_threshold|number (ms)|the minimal latency required to trigger (computed threshold will be raised to this value if needed)|None
|vol_pctile_req_pos|number (percentage)|percentage of historical window permitted to have request rate 0|90|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


It returns a detect block that triggers when the latency, suitably filtered and grouped,
over the last `current_window` is more than
`fire_num_dev_threshold` deviations from the norm (similarly filtered and grouped),
calculated on the preceding `historical_window`, and when volume conditions are met;
clears when latency is less than `clear_num_dev_threshold` deviations from the norm.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency.sudden_change_v2 import sudden_change

sudden_change.deviations_from_norm(filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~


#### Usage note

This should be considered documentation also for [workflows](../../workflow_latency/sudden_change_v2/sudden_change.flow), which sets `resource_type='workflow'`.
