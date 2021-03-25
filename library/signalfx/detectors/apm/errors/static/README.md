Detect when the error rate is larger than a specified static threshold.


## Detector

The `detector` function has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|current_window|duration|window on which error rate is calculated|duration('5m')|
|fire_rate_threshold|number|error rate needed to trigger, expressed as number between 0 and 1|0.01|
|clear_rate_threshold|number|error rate needed to clear, expressed as number between 0 and 1|0.001|
|attempt_threshold|integer|threshold on number of attempts (errors + non-errors) in the window being evaluated in order to trigger|1|
|filter_|filter|specifies dimensional scope of the detector|None|
|group_by|list of strings|group both errors and non-errors by these (in addition to default grouping by cluster, service, operation)|None|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|

It returns a detect block that triggers when the error rate for `filter_`, grouped by `group_by`, over the last `current_window` is greater than `fire_rate_threshold`, and when at least `attempt_threshold` requests were made over the last `current_window`; clears when the error rate is below `clear_rate_threshold`.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.errors.static import static

static.detector(fire_rate_threshold=0.05, clear_rate_threshold=0.02, filter_=filter('service', 'my_svc') and filter('operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~