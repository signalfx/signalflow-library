Detect when latency exceeds a static threshold.


## Detector

The `detector` function detects when latency exceeds a specified static threshold for a specified percent of duration. It has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|fire_threshold|number|latency threshold required to trigger, expressed in nanoseconds or milliseconds (see use_ms)|None|
|fire_lasting|lasting|percent of duration associated with fire_threshold|None|
|clear_threshold|numnber|latency threshold required to clear, expressed in nanoseconds or milliseconds (see use_ms)|None|
|clear_lasting|lasting|percent of duration associated with clear_threshold|None|
|use_ms|boolean|if True, use milliseconds; if False, use nanoseconds (see fire_threshold and clear_threshold)|True|
|pctile|number|percentile to monitor, one of 50, 90, 99|90|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|exclude_errors|boolean|whether to exclude error spans from latency metric|True|
|group_by|list of strings|average latency by these (in addition to default grouping associated with resource type)|None|    
|resource_type|string|key from [RESOURCE_TYPE_MAPPING](../../../apm/utils.flow), determines schema|'service_operation'|
|volume_static_threshold|number|threshold on request rate (per second) required for alert to trigger|None|
|volume_relative_threshold|number|require request rate on window being evaluated to be at least this proportion of request rate on preceding window (used for trigger and clear)|None|
|volume_nonzero_required|number between 0 and 1|require request rate to be nonzero for this proportion of fire_lasting.duration (used for trigger and clear)|0.1|    
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|

    
It returns detect block that triggers when the specified percentile of latency,
suitably filtered and grouped, exceeds the specified threshold for the required percent of duration;
and clears when latency remains below the specified clear threshold for the required percent of duration.




#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency.static_v2 import static

static.detector(100, lasting('3m', 0.8), 80, lasting('2m', 0.9)).publish('my_static_detector')
~~~~~~~~~~~~~~~~~~~~


#### Usage note

This should be considered documentation also for [workflows](../../workflow_latency/static_v2/static.flow), which sets `resource_type='workflow'`.
