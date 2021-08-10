The `requests` submodule of `apm` facilities the creation of alerts on request rates, as expressed in the `spans.count` metric.  
For example, one can detect when the request rate exceeds (or drops below) a static threshold,
when it grows too quickly relative to a recent or historical baseline,
or when it is too many deviations from a recent or historical norm.
 
#### Example usage

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.requests.sudden_change_v2 import sudden_change
from signalfx.detectors.apm.requests.historical_anomaly_v2 import historical_anomaly
from signalfx.detectors.apm.requests.static_v2 import static

f = filter('service', 'my_svc') and filter('operation', 'do_thing') and filter('sf_environment', 'prod')

sudden_change.detector_mean_std(filter_=f).publish('sudden_change_detector')
historical_anomaly.growth_rate(filter_=f).publish('historical_anomaly_detector')
static.detector(fire_threshold=4, fire_lasting=lasting('5m', 0.8), clear_threshold=3, clear_lasting=lasting('5m', 0.8), filter_=f).publish('static_threshold_detector')

~~~~~~~~~~~~~~~~~~~~

