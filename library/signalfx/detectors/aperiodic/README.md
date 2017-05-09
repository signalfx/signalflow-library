The `aperiodic` module contains functions that facilitate the creation of detectors that are insensitive to missing values and irregular arrival patterns. If one creates a detector that triggers when a stream `S` is above a threshold `T` for `100% of 5 minutes` (i.e. publishes `detect(when(S > T, '5m'))`), then `S` must be non-null and above `T` for all of the *expected* arrival times in a five-minute window. For example, if the resolution of `S` is calculated to be `10s`, then 30 datapoints are expected in a five-minute window. If 29 points, all above `T`, arrive in a five-minute window, the detector will *not* trigger. Moreover, the detector is subject to resolution calculation, which can cause difficulties for streams that do not publish at a regular cadence.

If instead one were to import this module and publish `aperiodic.one_sided_detector(S, T, lasting('5m', 1.0))`, the detector would trigger, as it requires 100% of the datapoints *received* in a five-minute window to be above the threshold.

This module is not currently exposed via the SignalFx UI. For all functions in this module, all parameters are required.                         

### Caution
Supposing `L` is a lasting object and `S` and `T` are as above, `detect(when(S > T, L))` and `aperiodic.one_sided_detector(S, T, L)` may behave differently when the duration of `L` is very large. This is because `aperiodic` is implemented via analytics with the duration of `L` as a transformation parameter, which influences the resolution of the resulting job. The job resulting from `detect(when(S > T, L))`, on the other hand, will have resolution dictated only by `S` and `T` even when the duration of `L` is large. In general the resolution of `aperiodic.one_sided_detector(S, T, L)` will be coarser than that of `detect(when(S > T, L))`. Similar comments apply to the other functions in this module.


### one_sided_detector

The `one_sided_detector` function has the following positional parameters. It returns a detect block that triggers when `stream1` is greater than `stream2` for `lasting`, ignoring missing values.

|Parameter name|Type|
|:---|:---|
|stream1|data stream or constant|
|stream2|data stream or constant|
|lasting|lasting|


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.aperiodic import aperiodic

cpu = data('cpu.utilization').mean()

aperiodic.one_sided_detector(cpu, 80, lasting('10m', 0.9)).publish('cpu_det_1')

~~~~~~~~~~~~~~~~~~~~


### one_sided_detector_with_clear

The `one_sided_detector_with_clear` function has the following positional parameters. It returns a detect block that triggers when `stream` is greater than 
 `fire_threshold` for `fire_lasting`, and clears when `stream` is less than `clear_threshold` for `clear_lasting`, ignoring missing values.

|Parameter name|Type|
|:---|:---|
|stream|data stream or constant|
|fire_threshold|data stream or constant|
|fire_lasting|lasting|
|clear_threshold|data stream or constant|
|clear_lasting|lasting|

Continuing the previous example, an example usage is as follows. This detector triggers when 90% of the values of `cpu` received in a 10-minute window are above 80, and it clears when 100% of the values received in a two-minute window are below 70.

~~~~~~~~~~~~~~~~~~~~
aperiodic.one_sided_detector_with_clear(cpu, 80, lasting('10m', 0.9), 70, lasting('2m', 1.0)).publish('cpu_det_2')

~~~~~~~~~~~~~~~~~~~~


### two_sided_detector

The `two_sided_detector` function has the following positional parameters. It returns a detect block that triggers when `stream` is greater than 
 `upper_stream` or less than `lower_stream` for `lasting`, ignoring missing values. In order to trigger, `stream` does not need to spend `lasting` in violation of only one of the two inequalities, so if it jumps back and forth between values greater than `upper_stream` and values lower than `lower_stream`, it will trigger.
 
|Parameter name|Type|
|:---|:---|
|stream|data stream or constant|
|upper_stream|data stream or constant|
|lower_stream|data stream or constant|
|lasting|lasting|


Continuing the previous example, an example usage is as follows. This detector triggers when 90% of the values of `cpu` received in a 10-minute window are either above 80, or below 20.

~~~~~~~~~~~~~~~~~~~~
aperiodic.two_sided_detector(cpu, 80, 20, lasting('10m', 0.9)).publish('cpu_det_3')

~~~~~~~~~~~~~~~~~~~~

### two_sided_detector_with_clear

The `two_sided_detector_with_clear` function has the following positional parameters. It returns a detect block that triggers when `stream` is greater than `fire_upper_stream` or less than `fire_lower_stream` for `fire_lasting`, and clears when `stream` is less than `clear_upper_stream` and greater than `clear_lower_stream` for `clear_lasting`, both ignoring missing values.

 
|Parameter name|Type|
|:---|:---|
|stream|data stream or constant|
|fire_upper_stream|data stream or constant|
|fire_lower_stream|data stream or constant|
|fire_lasting|lasting|
|clear_upper_stream|data stream or constant|
|clear_lower_stream|data stream or constant|
|clear_lasting|lasting|



Continuing the previous example, an example usage is as follows. This detector triggers when 90% of the values of `cpu` received in a 10-minute window are either above 80, or below 20, and it clears when 100% of the values received in a two-minute window are below 70 and above 30.

~~~~~~~~~~~~~~~~~~~~
aperiodic.two_sided_detector(cpu, 80, 20, lasting('10m', 0.9), 70, 30, lasting('2m', 1.0)).publish('cpu_det_4')

~~~~~~~~~~~~~~~~~~~~
    
