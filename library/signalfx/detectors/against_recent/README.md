The `against_recent` module contains four main functions. They detect when the recent values of a signal differ from the values of the immediately preceding time period. The SignalFx UI refers to this module as Sudden Change.


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
|calculation_mode|string|specifies whether to use exponentially weighted or usual moving average (options 'vanilla', 'ewma')|'vanilla'|
    
It returns a detect block that triggers when all the values of the last `current_window` of `stream` are at least `fire_num_stddev` standard deviations away from the mean of the preceding `historical_window`, and clears when all the values of the last `current_window` of `stream` remain within `clear_num_stddev` standard deviations of the mean of the preceding `historical_window`. The value of `orientation` determines whether the `current_window` is required to be above or below (or either) the norm established by the `historical_window`. Also, the value of `calculation_mode` determines whether the mean or an exponentially weighted moving average is used. 
    

#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_recent.detector_mean_std(service_cpu).publish('cpu_detector') # uses default values

against_recent.detector_mean_std(service_cpu, current_window=duration('3m'),
  historical_window=duration('2h'), fire_num_stddev=6).publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~

#### Streams and conditions

The thresholds used in this detector are given by `mean_std_thresholds` and the conditions are produced by `mean_std`. See `streams` itself for more intermediate calculations.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import streams
from signalfx.detectors.against_recent import conditions

s = data('cpu.utilization').mean()

fire_bot, clear_bot, clear_top, fire_top = streams.mean_std_thresholds(s)
detect(s.percentile(10, over='5m') > fire_top, s.percentile(80, over='5m') < clear_top).publish()

fire_cond, clear_cond = conditions.mean_std(s)
detect(when(s > 45, '10m') and fire_cond).publish()
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

It returns a detect block that triggers when all the values of the last `current_window` of `stream` exceed (or drop below) the `fire_percentile_threshold` percentile of the preceding `historical_window`, and clears when all the values of the last `current_window` of `stream` remain below (or above) the `clear_percentile_threshold` percentile of the preceding `historical_window`. The value of `orientation` determines whether the `current_window` is required to be above or below the norm established by the `historical_window`; the value 'out_of_band' detects change in either direction.

Implementation note: if 'below' is selected for `orientation`, the trigger threshold is the smaller of the `fire_percentile_threshold` and `100 - fire_percentile_threshold` percentiles, and the clear threshold is the smaller of the analogous quantities. Similarly, the larger of the two quantities is used when 'above' is selected. If 'out_of_band' is selected, the bands are symmetric about the value 50. The thresholds should satisfy `|fire_percentile_threshold - 50| >= |clear_percentile_threshold - 50|` for the detector to behave as expected.
    
   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_recent.detector_percentile(service_cpu).publish('cpu_detector') # uses default values

against_recent.detector_percentile(service_cpu, current_window=duration('3m'),
  historical_window=duration('2h'), fire_percentile_threshold=95, clear_percentile_threshold=85,
  orientation='out_of_band').publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~

#### Streams and conditions

The thresholds used in this detector are given by `percentile_thresholds` and the conditions are produced by `percentile`. See `streams` itself for more intermediate calculations.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import streams
from signalfx.detectors.against_recent import conditions

s = data('cpu.utilization').mean()

fire_bot, clear_bot, clear_top, fire_top = streams.percentile_thresholds(s)
detect(s.percentile(10, over='5m') > fire_top, s.percentile(80, over='5m') < clear_top).publish()

fire_cond, clear_cond = conditions.percentile(s)
detect(when(s > 30, '10m') and fire_cond).publish()
~~~~~~~~~~~~~~~~~~~~


## Mean plus percentage change

The `detector_growth_rate_vanilla` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|current_window|duration|window being tested for anomalous values|duration('5m')|
|historical_window|duration|window that defines normal values|duration('1h')|
|fire_growth_rate_threshold|number|percentage different from historical mean required to trigger, should be >= 0 |0.2|
|clear_growth_rate_threshold|number|percentage different from historical mean required to clear, should be >= 0|0.1|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|
|calculation_mode|string|specifies whether to use exponentially weighted or usual moving average (options 'vanilla', 'ewma')|'vanilla'|
    
It returns a detect block that triggers when all the values of the last `current_window` of `stream` are at least `100 * fire_growth_rate_threshold` % away from the mean of the preceding `historical_window`, and clears when all the values of the last `current_window` of `stream` remain within `100 * clear_growth_rate_threshold` % of the mean of the preceding `historical_window`. The value of `orientation` determines whether the `current_window` is required to be above or below (or either) the norm established by the `historical_window`. Also, the value of `calculation_mode` determines whether the mean or an exponentially weighted moving average is used. 
    
    

#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_recent.detector_growth_rate_vanilla(service_cpu).publish('cpu_detector') # uses default values

~~~~~~~~~~~~~~~~~~~~



#### Streams and conditions

The thresholds used in this detector are given by `growth_rate_thresholds` and the conditions are produced by `growth_rate`. See `streams` itself for more intermediate calculations.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import streams
from signalfx.detectors.against_recent import conditions

s = data('cpu.utilization').mean()

fire_bot, clear_bot, clear_top, fire_top = streams.growth_rate_thresholds(s)
detect(s.percentile(10, over='5m') > fire_top, s.percentile(80, over='5m') < clear_top).publish()

fire_cond, clear_cond = conditions.growth_rate(s)
detect(when(s > 45, '5m') and fire_cond).publish()
~~~~~~~~~~~~~~~~~~~~


