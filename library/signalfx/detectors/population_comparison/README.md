The `population_comparison` module contains two main functions. They detect when one member of a group of emitters is different from the norm of that group. The SignalFx UI refers to this module as Outlier Detection.

## Deviations from norm

The `detector` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|population_stream|stream|population being monitored for outliers|*None*|
|group_by_property|string or list of strings|dimension(s)/property(ies) by which to group the population|None|
|fire_num_dev|number|number of deviations from population norm required to trigger, should be >= 0|3|
|fire_lasting|lasting|percent of duration associated with trigger threshold|lasting('5m', 1.0)|
|clear_num_dev|number|number of deviations from population norm required to clear, should be >= 0|2.5|
|clear_lasting|lasting|percent of duration associated with clear threshold|lasting('5m', 1.0)|
|strategy|string|represents method for defining outliers, options 'mean_stddev' (mean plus standard deviation) and 'median_MAD' (median plus median absolute deviations)|'median_MAD'|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|
|denominator_mode|string|specifies whether to evaluate condition when data is expected, or when it actually arrives (options 'expected', 'observed')|'expected'|

It returns a detect block that triggers when a member of `population_stream` is more than `fire_num_dev` standard (resp. median absolute) deviations away from the population mean (resp. median) for `fire_lasting`, and clears when that member is within `clear_num_dev` standard (resp. median absolute) deviations away from the population mean (resp. median) for `clear_lasting`. The value of `strategy` determines whether mean plus standard deviation or median plus median absolute deviation is used, and `orientation` determines whether the member is required to be above or below (or either) the population norm.
    
   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.population_comparison import population

cpu = data('cpu.utilization')

# use this to compare each emitter to the entire population
population.detector(cpu).publish('cpu_detector_1')

# use this to compare each emitter to those with the same aws_tag_service
population.detector(cpu, group_by_property='aws_tag_service').publish('cpu_detector_2')

# this will compare aws_tag_services
service_cpu = data('cpu.utilization').mean(by='aws_tag_service')
population.detector(service_cpu).publish('cpu_detector_3')

~~~~~~~~~~~~~~~~~~~~

## Norm plus percentage change

The `detector_growth_rate` function has the following parameters. Parameters with no default value are required.                      

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|population_stream|stream|population being monitored for outliers|*None*|
|group_by_property|string or list of strings|dimension(s)/property(ies) by which to group the population|None|
|fire_growth_rate_threshold|number|percentage difference from population norm required to fire, should be >= 0|0.2|
|fire_lasting|lasting|percent of duration associated with trigger threshold|lasting('5m', 1.0)|
|clear_growth_rate_threshold|number|percentage difference from population norm required to clear, should be >= 0|0.1|
|clear_lasting|lasting|percent of duration associated with clear threshold|lasting('5m', 1.0)|
|strategy|string|represents method for defining norm, options 'mean' (mean) and 'median' (median)|'median'|
|orientation|string|specifies whether detect fires when signal is above, below, or out-of-band (options  'above', 'below', 'out_of_band')|'above'|
|denominator_mode|string|specifies whether to evaluate condition when data is expected, or when it actually arrives (options 'expected', 'observed')|'expected'|

It returns a detect block that triggers when a member of `population_stream` is more than `100 * fire_growth_rate_threshold` % away from the population mean (resp. median) for `fire_lasting`, and clears when that member is within `100 * clear_growth_rate_threshold` % of the population mean (resp. median) for `clear_lasting`. The value of `strategy` determines whether mean or median is used, and `orientation` determines whether the member is required to be above or below (or either) the population norm.
                            

#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.population_comparison import population

cpu = data('cpu.utilization')

population.detector_growth_rate(cpu).publish('cpu_detector_4')
