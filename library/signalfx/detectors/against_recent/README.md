The `against_recent` module contains two functions. Both detect when the recent values of a signal different from the values of the immediately preceding time period. One uses mean plus standard deviation to define a baseline, and the other uses a percentile. This SignalFx UI refers to this module as Sudden Change.


## Mean plus standard deviation

The `detector_mean_std` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|current_window|duration|window being tested for anomalous values|duration('5m')|
|historical_window|duration|window that defines normal values|duration('1h')|
|fire_num_stddev|number|number of standard deviations different from historical mean required to trigger, should be >= 0 |3|
|clear_num_stddev|number|number of standard deviations different from historical mean required to clear, should be >= 0|2.5|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|
    
It returns a detect block that triggers when the last `current_window` of `stream` is at least `fire_num_stddev` standard deviations above/below/away from the mean of the `preceding historical_window`, and clears when the last `current_window` of `stream` remains below/above/within `clear_num_stddev` standard deviations above/below/of the mean of the preceding `historical_window`.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_recent.detector_mean_std(service_cpu).publish('cpu_detector') # uses default values

against_recent.detector_mean_std(service_cpu, current_window=duration('3m'),
  historical_window=duration('2h'), fire_num_stddev=6).publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~


## Percentile

The `detector_percentile` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|current_window|duration|window being tested for anomalous values|duration('5m')|
|historical_window|duration|window that defines normal values|duration('1h')|
|fire_percentile_threshold|number|percentile of historical_window used as a trigger threshold, must be between 0 and 100|99|
|clear_percentile_threshold|number|percentile of historical_window used as a clear threshold, must be between 0 and 100|95|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|

It returns a detect block that fires when the last `current_window` of `stream` exceeds (or drops below, or goes out of band) the `fire_percentile_threshold` of the preceding `historical_window`, and clears when the last `current_window` of `stream` remains below (or above, or within band) the `clear_percentile_threshold` of the preceding `historical_window`.
    
   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_recent.detector_percentile(service_cpu).publish('cpu_detector') # uses default values

against_recent.detector_percentile(service_cpu, current_window=duration('3m'),
  historical_window=duration('2h'), fire_percentile_threshold=95, clear_percentile_threshold=85,
  orientation='out_of_band').publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~
