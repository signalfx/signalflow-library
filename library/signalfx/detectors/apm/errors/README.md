The `errors` submodule of `apm` captures the calculation of an error rate for a span over some duration. One can then detect when this error rate exceeds a static threshold (see [static](static_v2)) or when it grows too quickly (see [sudden_change](sudden_change_v2)). 


#### Streams and conditions

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.apm.errors import streams
from signalfx.detectors.apm.errors import conditions

f = filter('sf_service', 'my_svc') and filter('sf_operation', 'do_thing') and filter('sf_environment', 'prod')
dims = ['sf_environment', 'sf_service', 'sf_operation', 'sf_httpMethod', 'sf_kind']

# stream that calculates error rate over 5m
streams.error_rate(duration_=duration('5m'), filter_=f, use_kind_filter=False, r_up='sum', error_true=filter('sf_error', 'true'), error_false=filter('sf_error', 'false'), default_group_by=dims, default_allow_missing=dims).publish('error_rate')

c = conditions.error_rate_static(current_window=duration('15m'), filter_=f, fire_rate_threshold=0.1, clear_rate_threshold=0.05, use_kind_filter=False, r_up='sum', error_true=filter('sf_error', 'true'), error_false=filter('sf_error', 'false'), default_group_by=dims, default_allow_missing=dims)

# fire when error rate over 15m is > 10%, clear when < 5%
detect(c['on'], off=c['off']).publish('det')

# fire when error rate over 15m is > 10% OR when other_condition is met
detect(c['on'] or other_condition).publish('compound_det')
~~~~~~~~~~~~~~~~~~~~


