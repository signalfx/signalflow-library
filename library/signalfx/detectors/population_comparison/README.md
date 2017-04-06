The `population_comparison` module contains one main function. It detects when one member of a group of emitters is different from the norm of that group. This SignalFx UI refers to this module as Outlier Detection.

The `detector` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|population_stream|stream|data being monitored|*None*|
|group_by_property|string or list of strings|dimension(s)/property(ies) by which to group the population|None|
|fire_num_dev|number|number of deviations from population norm required to trigger|3|
|fire_lasting|lasting|percent of duration associated with trigger threshold|lasting('5m', 1.0)|
|clear_num_dev|number|number of deviations from population norm required to clear|2.5|
|clear_lasting|lasting|percent of duration associated with clear threshold|lasting('5m', 1.0)|
|strategy|string|represents method for defining outliers, options 'mean_stddev' (mean plus standard deviation) and 'median_MAD' (median plus median absolute deviations)|'median_MAD'|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|

It returns a detect block that triggers when a member of `population_stream` is more than `fire_num_dev` standard (resp. median absolute) deviations away from the population mean (resp. median) for `fire_lasting`, and clears when that member is within `clear_num_dev` standard (resp. median absolute) deviations away from the population mean (resp. median) for `clear_lasting`. The value of `strategy` determines whether mean plus standard deviation or median plus median absolute deviation is used, and `orientation` determines whether the member is required to be above or below (or either) the population norm.
    
   
#### Example usage FIXME
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_periods import against_periods

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_periods.detector_growth_rate(service_cpu).publish('cpu_detector') # uses default values

against_periods.detector_growth_rate(service_cpu, window_to_compare=duration('10m'),
  fire_growth_rate_threshold=0.3).publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~

                        

