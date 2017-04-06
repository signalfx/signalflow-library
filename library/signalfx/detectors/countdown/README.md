The `countdown` module contains two main functions. Both perform linear extrapolation on a signal and trigger when the extrapolation hits some value (0, or user-provided) within a certain number of hours. One function assumes the signal is increasing, and the other assumes it is decreasing. The SignalFx UI refers to this module as Resource Running Out.

The `hours_left_stream_detector` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream|assumed to be decreasing|*None*|
|lower_threshold|number|threshold for triggering (number of hours)|24|
|fire_lasting|lasting|lasting object associated with lower_threshold|lasting('10m', 1.0)|
|clear_threshold|number|threshold for clearing (number of hours)|36|
|clear_lasting|lasting|lasting object associated with clear threshold|lasting('10m', 1.0)|


It returns a detect block that triggers when the estimate that `stream` is projected to reach zero within `lower threshold` hours holds for `fire_lasting`, and clears when the estimated time left remains above `clear_threshold` hours for `clear_lasting`. The `stream` is assumed to be decreasing; periods during which `stream` increases count against it for the purposes of the `fire_lasting` parameter.

The `hours_left_stream_incr_detector` function has in addition a required `maximum_capacity` parameter; it returns a detect block that triggers when the estimate that `stream` is projected to reach `maximum_capacity` within `lower threshold` hours holds for `fire_lasting`, and clears when the estimated time left remains above `clear_threshold` hours for `clear_lasting`. Here, `stream` is assumed to be increasing. This function really just applies `hours_left_stream_detector` to the stream `maximum_capacity - stream`.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream|assumed to be increasing|*None*|
|maximum_capacity|number|value at which stream is exhausted|*None*|
|lower_threshold|number|threshold for triggering (number of hours)|24|
|fire_lasting|lasting|lasting object associated with lower_threshold|lasting('10m', 1.0)|
|clear_threshold|number|threshold for clearing (number of hours)|36|
|clear_lasting|lasting|lasting object associated with clear threshold|lasting('10m', 1.0)|

   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.countdown import countdown

countdown.hours_left_stream_incr_detector(data('disk.utilization'), 100).publish('disk_running_out')
~~~~~~~~~~~~~~~~~~~~




