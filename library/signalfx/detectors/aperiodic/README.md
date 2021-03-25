The `aperiodic` module contains functions that facilitate the creation of detectors that are insensitive to missing values and irregular arrival patterns. If one creates a detector that triggers when a stream `S` is above a threshold `T` for `100% of 5 minutes` (i.e. publishes `detect(when(S > T, '5m'))`), then `S` must be non-null and above `T` for all of the *expected* arrival times in a five-minute window. For example, if the resolution of `S` is calculated to be `10s`, then 30 datapoints are expected in a five-minute window. If 29 points, all above `T`, arrive in a five-minute window, the detector will *not* trigger. Moreover, the detector is subject to resolution calculation, which can cause difficulties for streams that do not publish at a regular cadence.

If instead one were to import this module and publish `aperiodic.above_or_below_detector(S, T, 'above', lasting('5m', 1.0))`, the detector would trigger, as it requires 100% of the datapoints *received* in a five-minute window to be above the threshold.

This module is not currently exposed via the SignalFx UI.

### Caution
Supposing `L` is a lasting object and `S` and `T` are as above, `detect(when(S > T, L))` and `aperiodic.above_or_below_detector(S, T, 'above', L)` may behave differently when the duration of `L` is very large. This is because `aperiodic` is implemented via analytics with the duration of `L` as a transformation parameter, which influences the resolution of the resulting job. The job resulting from `detect(when(S > T, L))`, on the other hand, will have resolution dictated only by `S` and `T` even when the duration of `L` is large. In general the resolution of `aperiodic.above_or_below_detector(S, T, 'above', L)` will be coarser than or equal to that of `detect(when(S > T, L))`. Similar comments apply to the other functions in this module.


### above_or_below_detector

The `above_or_below_detector` function returns a detect block that triggers when `stream` is greater than (or less than, depending on `orientation`) `threshold` for `observed_lasting`, ignoring missing values. One can optionally specify a second lasting object which additionally requires the inequality to hold for `expected_lasting`, including missing values. Non-strict inequalities are also supported.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream or constant|stream being monitored|-|
|threshold|data stream or constant|threshold against which stream is compared|-|
|orientation|string, one of 'above' or 'below'|whether to detect stream above or below threshold|-|
|observed_lasting|lasting|percentage of duration (excluding nulls)|-|
|expected_lasting|lasting (optional)|if specified, percentage of duration (including nulls)|None|
|annotations|list of annotate objects (optional)||None|
|event_annotations|dictionary (optional)||None|
|strict|boolean (optional)|if True, compare stream against threshold with strict inequality; if False, non-strict|True|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.aperiodic import aperiodic

cpu = data('cpu.utilization').mean()

aperiodic.above_or_below_detector(cpu, 80, 'above', lasting('10m', 0.9)).publish('cpu_above_80')

~~~~~~~~~~~~~~~~~~~~


### range_detector

The `range_detector` function returns a detect block that triggers when `stream` is out of (or within, depending on `orientation`) the range specified by `lower_threshold` and `upper_threshold` for `observed_lasting`, ignoring missing values. One can optionally specify a second lasting object which additionally requires the inequality to hold for `expected_lasting`, including missing values. (The out of range option actually means `stream` is less than `lower_threshold` or greater than `upper_threshold`, and the within range option actually means `stream` is greater than `lower_threshold` and less than `upper_threshold`.  Non-strict inequalities are also supported.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream or constant|stream being monitored|-|
|lower_threshold|data stream or constant|lower threshold of range|-|
|upper_threshold|data stream or constant|upper threshold of range|-|
|orientation|string, one of 'within_range', 'out_of_band'|whether to detect stream within or outside of range|-|
|observed_lasting|lasting|percentage of duration (excluding nulls)|-|
|expected_lasting|lasting (optional)|if specified, percentage of duration (including nulls)|None|
|annotations|list of annotate objects (optional)||None|
|event_annotations|dictionary (optional)||None|
|lower_strict|boolean (optional)|if True, compare stream against lower with strict inequality; if False, non-strict|True|
|upper_strict|boolean (optional)|if True, compare stream against upper with strict inequality; if False, non-strict|True|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema or has value None|None|


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.aperiodic import aperiodic

cpu = data('cpu.utilization').mean()

aperiodic.range_detector(cpu, 20, 80, 'out_of_band', lasting('10m', 0.9)).publish('cpu_outside_20_80')

~~~~~~~~~~~~~~~~~~~~


There are enhancements to the above, namely `above_or_below_detector_with_clear` and `range_detector_with_clear`, which also allow for the specification of clear conditions. These functions require separate "threshold" and "lasting" parameters to specify the fire and clear conditions. Distinct "strict" parameters are also accepted (with all defaulting to strict inequalities, i.e., value `True`.)