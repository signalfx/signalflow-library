The `countdown` module contains functions for forecasting when a resource is likely to be exhausted. The SignalFx UI refers to this module as Resource Running Out.


The first two functions perform linear extrapolation on a signal and trigger when the extrapolation hits some value within a certain number of hours.
One function assumes the signal is increasing, and the other assumes it is decreasing. 

The `hours_left_stream_detector` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream|assumed to be decreasing|*None*|
|minimum_value|number|value at which stream is considered empty|0|
|lower_threshold|number|threshold for triggering (number of hours), should be > 0|24|
|fire_lasting|lasting|lasting object associated with lower_threshold|lasting('10m', 1.0)|
|clear_threshold|number|threshold for clearing (number of hours), should be > 0|36|
|clear_lasting|lasting|lasting object associated with clear threshold|lasting('10m', 1.0)|
|use_double_ewma|boolean|whether to use double_ewma to forecast (True uses it, False uses linear extrapolation)|False|
|damping|number|damping factor to use (only relevant if use_double_ewma=True), must be between 0 and 1|1.0|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


It returns a detect block that triggers when the estimate that `stream` is projected to reach zero within `lower threshold` hours holds for `fire_lasting`, and clears when the estimated time left remains above `clear_threshold` hours for `clear_lasting`. The `stream` is assumed to be decreasing; periods during which `stream` increases count against it for the purposes of the `fire_lasting` parameter.

The `hours_left_stream_incr_detector` function has in addition a required `maximum_capacity` parameter; it returns a detect block that triggers when the estimate that `stream` is projected to reach `maximum_capacity` within `lower threshold` hours holds for `fire_lasting`, and clears when the estimated time left remains above `clear_threshold` hours for `clear_lasting`. Here, `stream` is assumed to be increasing. This function really just applies `hours_left_stream_detector` to the stream `maximum_capacity - stream`.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream|assumed to be increasing|*None*|
|maximum_capacity|number|value at which stream is exhausted|*None*|
|lower_threshold|number|threshold for triggering (number of hours), should be > 0|24|
|fire_lasting|lasting|lasting object associated with lower_threshold|lasting('10m', 1.0)|
|clear_threshold|number|threshold for clearing (number of hours), should be > 0|36|
|clear_lasting|lasting|lasting object associated with clear threshold|lasting('10m', 1.0)|
|use_double_ewma|boolean|whether to use double_ewma to forecast (True uses it, False uses linear extrapolation)|False|
|damping|number|damping factor to use (only relevant if use_double_ewma=True), must be between 0 and 1|1.0|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|

   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.countdown import countdown

countdown.hours_left_stream_incr_detector(data('disk.utilization'), 100).publish('disk_running_out')
~~~~~~~~~~~~~~~~~~~~



There is also a function that uses the forecast capability of double exponential smoothing. 

The `hours_left_stream_dewma_detector` function has the following parameters; it returns a detect block that triggers when the estimate that `stream` is projected to reach `stream_threshold` within `lower threshold` hours holds for `fire_lasting`, and clears when the estimated time left remains above `clear_threshold` hours for `clear_lasting`. Here, `stream` is assumed to be increasing if `orientation='to_capacity'` and decreasing if `orientation='to_empty'`.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream|assumed to be increasing|*None*|
|stream_threshold|number|value at which stream is exhausted|0|
|orientation|string|whether to detect stream reaching empty or capacity (options 'to_empty', 'to_capacity')|'to_empty'|
|lower_threshold|duration|threshold for triggering|duration('24h')|
|fire_lasting|lasting|lasting object associated with lower_threshold|lasting('10m', 1.0)|
|clear_threshold|duration|threshold for clearing|duration('36h')|
|clear_lasting|lasting|lasting object associated with clear threshold|lasting('10m', 1.0)|
|alpha|number|smoothing parameter for the level term, must be between 0 and 1|0.1|
|beta|number|smoothing parameter for the trend term, must be between 0 and 1|0.1|
|damping|number|damping parameter for forecasting, must be between 0 and 1|1.0|
|use_duration|boolean|if False, uses alpha and beta provided; if True, uses 5 * max(fire_lasting.duration, clear_lasting.duration) as double_ewma parameter|False|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|



#### Streams and conditions

The streams used in these detectors are given by `hours_left_stream`, `hours_left_stream_incr`, and `hours_left_dewma_streams`; and the conditions are produced by `hours_left_stream_conditions` and `hours_left_stream_incr_conditions` (these may call `hours_left_stream_dewma_conditions`, which is also exposed).

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.countdown import streams
from signalfx.detectors.countdown import conditions

s = data('memory.utilization')

hours_left = streams.hours_left_stream_incr(s, 100)
detect(hours_left.max() < 24).publish('all_running_out_of_memory')

fire_cond, clear_cond = conditions.hours_left_stream_incr_conditions(s, 95)
detect(when(s > 90, '20m') or fire_cond).publish()
~~~~~~~~~~~~~~~~~~~~
