The `confidence_intervals` module calculates confidence intervals that determine the range of values
in which the true population parameters are likely to fall for a given level of confidence.
A z_score parameter may be passed in to set the confidence level, else it defaults to 1.96 for 95%.

The `wilson` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|n|stream|sample size|*None*|
|successes|stream|number of successes|*None*|
|z_score|number|z corresponding to confidence level|1.96|


The return value is a tuple of streams. The first element is the upper bound of the confidence interval
and the second element is the lower bound.

|Index|Type|Description of content|
|:---|:---|:---|
|0|stream|upper bound|
|1|stream|lower bound|


#### Example usage

~~~~~~~~~~~~~~~~~~~~
from signalfx.stats.confidence_intervals import binomial_proportion

failures = data('api.failures').sum().sum(over='1h')
successes = data('api.successes').sum().sum(over='1h')
n = successes + failures

upper_bound, lower_bound = binomial_proportion.wilson(n, successes, z_score = 2.576)
~~~~~~~~~~~~~~~~~~~~


#### Notes

The streams passed in may use the sum(over=window) analytic, where window is used to define
the a rolling time window for the confidence interval bounds.

