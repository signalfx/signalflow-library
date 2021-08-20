Detect when the error ratio is larger than a specified static threshold.

## Detector

The `detector` function has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|current_window|duration|window on which error ratio is calculated|duration('5m')|
|fire_rate_threshold|number|error ratio needed to trigger, expressed as number between 0 and 1|0.01|
|clear_rate_threshold|number|error ratio needed to clear, expressed as number between 0 and 1|0.001|
|attempt_threshold|integer|threshold on number of attempts (errors + non-errors) in the window being evaluated in order to trigger|1|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|group_by|list of strings|group both errors and non-errors by these (in addition to default grouping associated with resource type)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING](../../../apm/utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


It returns a detect block that triggers when the error ratio for `filter_ and custom_filter`, grouped by `group_by` (and the default), over the last `current_window` is greater than `fire_rate_threshold`, and when at least `attempt_threshold` requests were made over the last `current_window`; clears when the error ratio is below `clear_rate_threshold`.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.errors.static_v2 import static

static.detector(fire_rate_threshold=0.05, clear_rate_threshold=0.02, filter_=filter('sf_service', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~


#### Usage note

This should be considered documentation also for [workflows](../../workflow_errors/static_v2/static.flow), which sets `resource_type='workflow'`.