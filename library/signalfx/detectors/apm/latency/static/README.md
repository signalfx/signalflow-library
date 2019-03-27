Detect when latency exceeds a static threshold


## Detector

The `detector` function detects when latency exceeds a specified static threshold for a specified percent of duration. It has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|fire_threshold|number|latency threshold required to trigger, expressed in FIXME|*None*|
|fire_lasting|lasting|percent of duration associated with fire_threshold|*None*|
|clear_threshold|numnber|latency threshold required to clear, expressed in FIXME|*None*|
|clear_lasting|lasting|percent of duration associated with clear_threshold|*None*|
|pctile|number|percentile to monitor, one of 50, 90, 99|90|
|filter_|filter|specifies dimensional scope of the detector|None|
|exclude_errors|boolean|whether to exclude error spans from latency metric|True|
|group_by|list of strings|average latency by these (in addition to default grouping by cluster, service, operation)|None|    
|volume_static_threshold|||FIXME|
|volume_pct_threshold|||FIXME|
|volume_nonzero_required|||FIXME|

It returns detect block that triggers when the specified percentile of latency,
suitably filtered and grouped, exceeds the specified threshold for the required percent of duration;
and clears when latency remains below the specified clear threshold for the required percent of duration.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency.static import static

static.detector(100, lasting('3m', 0.8), 80, lasting('2m', 0.9)).publish('my_static_detector')
~~~~~~~~~~~~~~~~~~~~
