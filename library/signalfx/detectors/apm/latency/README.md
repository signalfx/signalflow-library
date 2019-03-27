The `latency` submodule of `apm` 

... as expressed in the `spans.duration.ns.*` metrics.
  
One can then detect when latency exceeds a static threshold (see `static`),
when it grows too quickly relative to a recent (see `sudden_change.growth_rate`) or historical ( `historical_anomaly.growth_rate`) baseline,
or when it is too many deviations from a recent (see `sudden_change.deviations_from_norm`) or historical ( `historical_anomaly.deviations_from_norm`) norm.
 
 





#### Streams and conditions

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency import streams
from signalfx.detectors.apm.latency import conditions


f = filter('service', 'my_svc') and filter('operation', 'do_thing')





FIXME
# stream that calculates error rate over 5m
streams.error_rate(duration_=duration('5m'), filter_=f).publish('error_rate')


c = conditions.error_rate_static(current_window=duration('15m'), filter_=f, fire_rate_threshold=0.1, clear_rate_threshold=0.05)

# fire when error rate over 15m is > 10%, clear when < 5%
detect(c['on'], off=c['off']).publish('det')

# fire when error rate over 15m is > 10% OR when other_condition is met
detect(c['on'] or other_condition).publish('compound_det')
FIXME

~~~~~~~~~~~~~~~~~~~~


