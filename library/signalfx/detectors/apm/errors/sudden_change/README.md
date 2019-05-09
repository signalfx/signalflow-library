Detect when the error rate grows by a specified amount.


## Detector

The `detector` function detect when the error rate grows by a specified amount and has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|current_window|duration|window whose error rate is evaluated for being too high|duration('5m')|
|preceding_window|duration|window whose error rate is used to define a baseline|duration('1h')|
|fire_growth_threshold|number|error rate growth required to trigger (default 0.5 corresponds to 50% growth)|0.5|
|clear_growth_threshold|number|error rate growth required to clear|0.1|
|attempt_threshold|integer|threshold on number of attempts (errors + non-errors) in the window being evaluated in order to trigger|1|
|filter_|filter|specifies dimensional scope of the detector|None|
|group_by|list of strings|group both errors and non-errors by these (in addition to default grouping by cluster, service, operation)|None|

It returns a detect block that triggers when the error rate for `filter_`, grouped by `group_by`, over the last `current_window` is greater than `1 + fire_growth_threshold` times the error rate of the preceding `preceding_window`, and when at least `attempt_threshold` requests were made over the last `current_window`; clears when the error rate is less than `1 + clear_growth_threshold` times the baseline error rate.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.errors.sudden_change import sudden_change

sudden_change.detector(filter_=filter('service', 'my_svc') and filter('operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~