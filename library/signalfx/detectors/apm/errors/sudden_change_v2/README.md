Detect when the error ratio grows by a specified amount.


## Detector

The `detector` function detect when the error ratio grows by a specified amount and has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|current_window|duration|window whose error ratio is evaluated for being too high|duration('5m')|
|preceding_window|duration|window whose error ratio is used to define a baseline|duration('1h')|
|fire_growth_threshold|number|error ratio growth required to trigger (default 0.5 corresponds to 50% growth)|0.5|
|clear_growth_threshold|number|error ratio growth required to clear|0.1|
|attempt_threshold|integer|threshold on number of attempts (errors + non-errors) in the window being evaluated in order to trigger|1|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|group_by|list of strings|group both errors and non-errors by these (in addition to default grouping associated with resource type)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|             
             

It returns a detect block that triggers when the error ratio for`filter_ and custom_filter`, grouped by `group_by` (and the default), over the last `current_window` is greater than `1 + fire_growth_threshold` times the error ratio of the preceding `preceding_window`, and when at least `attempt_threshold` requests were made over the last `current_window`; clears when the error ratio is less than `1 + clear_growth_threshold` times the baseline error ratio.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.errors.sudden_change_v2 import sudden_change

sudden_change.detector(filter_=filter('sf_service', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~



#### Usage note

This should be considered documentation also for [workflows](../../workflow_errors/sudden_change_v2/sudden_change.flow), which sets `resource_type='workflow'`.
