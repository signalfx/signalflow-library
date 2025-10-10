Detect when the request rate exhibits a sudden increase or decrease.


## Growth rate

The `detector_growth_rate` function detects when the request rate grows or decays by a specified amount relative to the preceding window. It has the following parameters.

| Parameter name            |Type|Description|Default value|
|:--------------------------|:---|:---|:---|
| filter_                   |filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
| exclude_errors            |boolean|whether to exclude error spans from the request rate|False|
| group_by                  |list of strings|sum by these (in addition to default grouping associated with resource type)|None|
| custom_filter             |filter|specifies dimensional scope of the detector (on custom dimensions)|None|
| current_window            |duration|window whose request rate is evaluated for being too high|duration('5m')|
| historical_window         |duration|window whose request rate is used to define the baseline|duration('1h')|
| fire_growth_rate_threshold|number|request rate growth required to trigger|0.2|
| clear_growth_rate_threshold|number|request rate growth required to clear|0.1|
| orientation               |string|specifies whether detect fires when request rate is above or below threshold (options  'above', 'below')|'above'|
| calculation_mode          |string|specifies whether to use exponentially weighted or usual moving average (options 'vanilla', 'ewma')|'ewma'|
| resource_type             |string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
| auto_resolve_after        |duration|if provided, duration after which to clear when group drops from schema or has value None|None|
| fire_lasting              |lasting|duration for which the trigger threshold must be met before the detector fires an alert|None|

It returns a detect block that triggers when all of the values of request rate, suitably filtered and grouped, over the last `current_window`, are greater than `1 + fire_growth_rate_threshold` times the request rate of the preceding `historical_window`;
and clears when the request rate is less than `1 + clear_growth_rate_threshold` times the baseline, assuming `orientation` is `'above'`. 
   

#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.requests.sudden_change_v2 import sudden_change

sudden_change.detector_growth_rate(filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~

    
## Mean plus standard deviation
                      
The `detector_mean_std` function detects when the request rate is too many deviations from the norm established in the preceding window. It has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|exclude_errors|boolean|whether to exclude error spans from the request rate|False|
|group_by|list of strings|sum by these (in addition to default grouping associated with resource type)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|current_window|duration|window whose request rate is evaluated for being too high|duration('5m')|
|historical_window|duration|window whose request rate is used to define the baseline|duration('1h')|
|fire_num_stddev|number|number of standard deviations different from historical mean required to trigger, should be >= 0 |3|
|clear_num_stddev|number|number of standard deviations different from historical mean required to clear, should be >= 0|2.5|
|orientation|string|specifies whether detect fires when request rate is above or below threshold (options  'above', 'below')|'above'|
|ignore_extremes|boolean|specifies whether to filter the historical_window by excluding points more than fire_num_stddev/clear_num_stddev away from the mean before calculating the band|True|
|calculation_mode|string|specifies whether to use exponentially weighted or usual moving average (options 'vanilla', 'ewma')|'ewma'|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


It returns a detect block that triggers when all of the values of request rate, suitably filtered and grouped,
over the last `current_window`, are more than`fire_num_stddev` standard deviations from the mean (above or below depending on the value of `orientation`) calculated on the preceding `historical_window`; clears when the request rate is less than `clear_num_stddev` deviations from the mean.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.requests.sudden_change_v2 import sudden_change

sudden_change.detector_mean_std(filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~


#### Usage note

This should be considered documentation also for [workflows](../../workflow_requests/sudden_change_v2/sudden_change.flow), which sets `resource_type='workflow'`.