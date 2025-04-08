Detect when the request rate exceeds or drops below a static threshold.

## Detector

The `detector` function has the following parameters.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|fire_threshold|number|request rate required to trigger, expressed as a rate (per second)|None|
|fire_lasting|lasting|percent of duration associated with fire_threshold|None|
|clear_threshold|number|request rate required to clear, expressed as a rate (per second)|None|
|clear_lasting|lasting|percent of duration associated with clear_threshold|None|
|orientation|string|specifies whether detect fires when request rate is above or below threshold (options  'above', 'below')|'above'|
|filter_|filter|specifies dimensional scope of the detector (on built-in dimensions)|None|
|exclude_errors|boolean|whether to exclude error spans from the request rate|False|
|group_by|list of strings|sum by these (in addition to default grouping associated with resource type)|None|
|custom_filter|filter|specifies dimensional scope of the detector (on custom dimensions)|None|
|resource_type|string|key from [RESOURCE_TYPE_MAPPING_HISTOGRAMS](../../utils.flow), determines schema|'service_operation'|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


It returns a detect block that triggers when the request rate for `filter_ and custom_filter`, grouped by `group_by` (and the default), either exceeds or drops below (depending on `orientation`) the threshold `fire_threshold` for `fire_lasting`; and clears based on the opposite behavior with respect to `clear_threshold` and `clear_lasting`.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.requests.static_v2 import static

static.detector(fire_threshold=88, fire_lasting=lasting('2m', 0.9), clear_threshold=71, clear_lasting=lasting('1m', 0.9), filter_=filter('service.name', 'my_svc') and filter('sf_operation', 'my_op')).publish('my_det')
~~~~~~~~~~~~~~~~~~~~


#### Usage note

This should be considered documentation also for [workflows](../../workflow_requests/static_v2/static.flow), which sets `resource_type='workflow'`.
