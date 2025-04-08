Detect when the request rate differs from a historically defined baseline.

## Growth rate

The `detector_growth_rate` function detects when the request rate grows or decays by a specified amount relative to the historical baseline. It has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|exclude_errors|boolean|whether to exclude error spans from the request rate|False|
|group_by|list of strings|sum by these (in addition to default grouping associated with resource type)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|window_to_compare|duration|length of current window (being tested for anomalous values), and historical windows (used to establish a baseline)|duration('15m')|
|space_between_windows|duration|time range reflecting the periodicity of the data stream|duration('1w')|  
|num_windows|integer|number of previous periods used to define baseline, must be > 0|4|
|fire_growth_rate_threshold|number|request rate growth required to trigger|0.2|
|clear_growth_rate_threshold|number|request rate growth required to clear|0.1|
|discard_historical_outliers|boolean|whether to take the median (True) or mean (False) of historical windows|True|
|orientation|string|specifies whether detect fires when request rate is above or below threshold (options  'above', 'below')|'above'|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|

    
It returns a detect block that triggers when the average request rate, suitably filtered and grouped, over the last `window_to_compare`, is greater than `1 + fire_growth_rate_threshold` times the historically defined baseline request rate;
and clears when the request rate is less than `1 + clear_growth_rate_threshold` times the baseline, , assuming `orientation` is `'above'`. 
   

#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.requests.historical_anomaly_v2 import historical_anomaly

historical_anomaly.detector_growth_rate(filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~

    
## Mean plus standard deviation
                      
The `detector_mean_std` function detects when the request rate is too many deviations from the historically defined norm. It has the following parameters.
    
|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|exclude_errors|boolean|whether to exclude error spans from the request rate|False|
|group_by|list of strings|sum by these (in addition to default grouping associated with resource type)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|window_to_compare|duration|length of current window (being tested for anomalous values), and historical windows (used to establish a baseline)|duration('15m')|
|space_between_windows|duration|time range reflecting the periodicity of the data stream|duration('1w')|
|num_windows|integer|number of previous periods used to define baseline, must be > 0|4|
|fire_num_stddev|number|number of standard deviations different from historical mean required to trigger, should be >= 0 |3|
|clear_num_stddev|number|number of standard deviations different from historical mean required to clear, should be >= 0|2.5|
|discard_historical_outliers|boolean|whether to take the median (True) or mean (False) of historical windows in case calculation_mode='within'; whether to take trimmed (True) or untrimmed (False) mean in case calculation_mode='across'|True|
|calculation_mode|string|whether to calculate standard deviations across periods ('across') or within periods ('within')|'across'|
|orientation|string|specifies whether detect fires when request rate is above or below threshold (options  'above', 'below')|'above'|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|

It returns a detect block that triggers when the average request rate, suitably filtered and grouped,
over the last `window_to_compare`, is more than`fire_num_stddev` standard deviations from the mean (above or below depending on the value of `orientation`) calculated on historical data; clears when the request rate is less than `clear_num_stddev` deviations from the mean.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.requests.historical_anomaly_v2 import historical_anomaly

historical_anomaly.detector_mean_std(filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~


#### Usage note

This should be considered documentation also for [workflows](../../workflow_requests/sudden_change_v2/sudden_change.flow), which sets `resource_type='workflow'`.
