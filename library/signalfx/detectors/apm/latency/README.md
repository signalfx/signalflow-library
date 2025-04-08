The `latency` submodule of `apm` facilities the creation of alerts on span latency, as expressed in the `spans` histogram metric.  
For example, one can detect when latency exceeds a static threshold (see [static](../latency/static_v2/README.md)),
when it grows too quickly relative to a recent (see [growth_rate](../latency/sudden_change_v2/README.md)) or historical (see [growth_rate](../latency/historical_anomaly_v2/README.md)) baseline,
or when it is too many deviations from a recent (see [deviations_from_norm](../latency/sudden_change_v2/README.md)) or historical (see [deviations_from_norm](../latency/historical_anomaly_v2/README.md)) norm.
 
#### Streams and conditions

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.latency import conditions

f = filter('service.name', 'my_svc') and filter('sf_operation', 'do_thing') and filter('deployment.environment', 'prod')
dims = ['deployment.environment', 'service.name', 'sf_operation', 'sf_httpMethod', 'sf_kind']
eef = not filter('sf_error', 'true')

# uses recent data as baseline
sc_conds = conditions.growth_rate_sc_histograms(filter_=f, use_kind_filter=False, exclude_errors_filter=eef, default_group_by=dims, default_allow_missing=dims)

# uses historical data as baseline
ha_conds = conditions.growth_rate_ha_histograms(filter_=f, use_kind_filter=False, exclude_errors_filter=eef, default_group_by=dims, default_allow_missing=dims)

# trigger when either threshold is met, clear when both are back to normal
detect(sc_conds['on'] or ha_conds['on'], off=sc_conds['off'] and ha_conds['off']).publish('compound_det')
~~~~~~~~~~~~~~~~~~~~

