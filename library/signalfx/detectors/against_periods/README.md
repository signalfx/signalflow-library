The `against_periods` module contains two main functions. Both detect when the recent values of a signal differ from its historical values. One uses mean plus standard deviation to construct a threshold from historical values, and the other uses mean plus percentage change. The SignalFx UI refers to this module as Historical Anomaly.



## Mean plus percentage change

The `detector_growth_rate` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|window_to_compare|duration|length of current window (being tested for anomalous values), and historical windows (used to establish a baseline)|duration('15m')|
|space_between_windows|duration|time range reflecting the cyclicity of the data stream|duration('1w')|
|num_windows|integer|number of previous cycles used to define baseline, must be > 0|4|
|fire_growth_rate_threshold|number|change over historical norm required to fire, should be >= 0|0.2|
|clear_growth_rate_threshold|number|change over historical norm required to clear, should be >= 0|0.1|
|discard_historical_outliers|boolean|whether to take the median (True) or mean (False) of historical windows|True|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|

It returns a detect block that triggers when the mean of the last `window_to_compare` of `stream` differs from the historical norm of `stream`. The historical norm is formed from the previous `num_windows` periods of length `window_to_compare`, spaced `space_between_windows` apart. Take either the median (`discard_historical_outliers`=True) or the mean (`discard_historical_outliers`=False) of the `num_periods` historical means. This triggers when the current value is `fire_growth_rate_threshold` larger (or smaller, or either, depending on the value of `orientation`) than the historical norm and clears when the current value is within `clear_growth_rate_threshold` of the historical norm.
   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_periods import against_periods

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_periods.detector_growth_rate(service_cpu).publish('cpu_detector') # uses default values

against_periods.detector_growth_rate(service_cpu, window_to_compare=duration('10m'),
  fire_growth_rate_threshold=0.3).publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~

                         
## Mean plus standard deviation

The `detector_mean_std` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|window_to_compare|duration|length of current window (being tested for anomalous values), and historical windows (used to establish a baseline)|duration('15m')|
|space_between_windows|duration|time range reflecting the cyclicity of the data stream|duration('1w')|
|num_windows|integer|number of previous cycles used to define baseline, must be > 0|4|
|fire_num_stddev|number|number of standard deviations from historical mean required to trigger, should be >= 0|3|
|clear_num_stddev|number|number of standard deviations from historical mean required to clear, should be >= 0|2.5|
|calculation_mode|string|whether to calculate standard deviations across periods ('across') or within periods ('within')|'within'|
|discard_historical_outliers|boolean|whether to take the median (True) or mean (False) of historical windows in case calculation_mode='within'; whether to take trimmed (True) or untrimmed (False) mean in case calculation_mode='across'|True|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|

It returns a detect block that triggers when the mean of the last `window_to_compare` of `stream` differs from the historical norm of `stream`. The historical norm is formed from the previous `num_windows` periods of length `window_to_compare`, spaced `space_between_windows` apart. For `calculation_mode='within'`, to define a trigger threshold, take either the median (`discard_historical_outliers`=True) or the mean (`discard_historical_outliers`=False) of the `num_periods` historical mean + `fire_num_stddev` standard deviations. For `calculation_mode='across'`, to define a trigger threshold, take the mean + `fire_num_stddev` standard deviations across all `num_periods` periods (`discard_historical_outliers`=False), or across the `num_periods - 2` periods gotten by discarding the periods with largest and smallest mean (`discard_historical_outliers`=True).

Use the same procedure with `clear_num_stddev` for the clear threshold. This triggers when the current value is larger (or smaller, or either, depending on the value of `orientation`) than the historically defined trigger threshold and clears when the current value is on the corresponding side of the clear threshold.

#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_periods import against_periods

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_periods.detector_mean_std(service_cpu).publish('cpu_detector') # uses default values

against_periods.detector_mean_std(service_cpu, window_to_compare=duration('10m'),
  fire_num_stddev=4, discard_historical_outliers=False).publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~


