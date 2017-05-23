The `multivariate` module at present contains one function, `correlation_coefficient`, which calculates the (Pearson) correlation coefficient between two streams. Its positional parameters, all of which are required, are as follows.

|Parameter name|Type|
|:---|:---|
|stream1|data stream|
|stream2|data stream|
|duration|duration|

It returns a data stream whose value is the correlation coefficient between `stream1` and `stream2` during the preceding `duration`. This is a number between -1 and 1. Using the correlation coefficient as an argument to a detector allows for alerts based on the relationship between two data streams.


#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.multivariate import correlation
from signalfx.detectors.against_recent import against_recent

cpu_1 = data('cpu.utilization', filter=filter('aws_tag_service', 'svc-1')).mean()
cpu_2 = data('cpu.utilization', filter=filter('aws_tag_service', 'svc-2')).mean()
corr_coeff = correlation.correlation_coefficient(cpu_1, cpu_2, duration('30m'))

# detects when the 30-minute correlation between svc-1 cpu and svc-2 cpu suddenly increases
against_recent.detector_percentile(corr_coeff, historical_window=duration('2h')).publish('correlation_changed')

~~~~~~~~~~~~~~~~~~~~