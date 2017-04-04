The `against_periods` module contains two functions. Both detect when the recent values of a signal different from its historical values. One uses mean plus standard deviation to construct a threshold from historical values, and the other uses mean plus percentage change. This SignalFx UI refers to this module as Historical Anomaly.



## Mean plus percentage change

The `detector_growth_rate` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|window_to_compare|duration|length of current window (being tested for anomalous values), and historical windows (used to establish a baseline)|duration('15m')|
|space_between_windows|duration|time range reflecting the cyclicity of the data stream|duration('1w')|
|num_windows|number|number of previous cycles used to define baseline|4|
|fire_growth_rate_threshold|number|change over historical norm required to fire|0.2|
|clear_growth_rate_threshold|number|change over historical norm required to clear|0.1|
|discard_historical_outliers|boolean|whether to take the median (True) or mean (False) of historical windows|True|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|

It returns a detect block that triggers when the ........
    
   
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
|num_windows|number|number of previous cycles used to define baseline|4|
|fire_num_stddev|number|number of standard deviations from historical mean required to trigger|3|
|clear_num_stddev|number|number of standard deviations from historical mean required to clear|2.5|
|discard_historical_outliers|boolean|whether to take the median (True) or mean (False) of historical windows|True|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|

It returns a detect block that triggers when ...


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_periods import against_periods

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_periods.detector_mean_std(service_cpu).publish('cpu_detector') # uses default values

against_periods.detector_mean_std(service_cpu, window_to_compare=duration('10m'),
  fire_num_stddev=4, discard_historical_outliers=False).publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~


