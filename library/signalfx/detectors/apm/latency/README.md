The `latency` submodule of `apm` facilities the creation of alerts on span latency, as expressed in the `spans.duration.ns.*` metrics.  
For example, one can detect when latency exceeds a static threshold (see `static`),
when it grows too quickly relative to a recent (see `sudden_change.growth_rate`) or historical ( `historical_anomaly.growth_rate`) baseline,
or when it is too many deviations from a recent (see `sudden_change.deviations_from_norm`) or historical ( `historical_anomaly.deviations_from_norm`) norm.
 

#### Streams and conditions

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency import conditions

f = filter('service', 'my_svc') and filter('operation', 'do_thing')


# uses recent data as baseline
sc_conds = conditions.growth_rate_sc(filter_=f)

# uses historical data as baseline
ha_conds = conditions.growth_rate_ha(filter_=f)

# trigger when either threshold is met, clear when both are back to normal
detect(sc_conds['on'] or ha_conds['on'], off=sc_conds['off'] and ha_conds['off']).publish('compound_det')
~~~~~~~~~~~~~~~~~~~~


