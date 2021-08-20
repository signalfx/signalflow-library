The `apm` module consists primarily of the submodules `errors`, `latency`, and `requests`, providing a package of alerts on the standard RED metrics.


#### Differences with the rest of the SignalFlow Library

The functions in the `apm` module operate on metrics with a known meaning and metadata. As a consequence, it is possible to develop somewhat tailored alerting strategies.

Some of the principal differences are as follows:

- Whereas the functions appearing in `against_recent`, `against_periods`, `aperiodic`, `countdown`, and `not_reporting` generally take an input stream as an argument, the functions in the `apm` module do not take input streams. Rather, they take filters and other parameters, and these produce data blocks that are passed to statistically-oriented procedures.
- Since the APM metrics consist of percentiles and counts, the patterns do not have the same general applicability as those captured in the modules mentioned above. For example, an estimate of the spread of a distribution can be obtained by taking the difference between percentiles, and an alert can be conditioned on the volume of traffic (captured in the metric `spans.count`) via a compound condition. Of course, the patterns do apply to other scenarios in which percentiles are emitted as metrics (replacing the metrics `spans.duration.ns.*` and `spans.count` as appropriate), and indeed the modules for workflows and RUM metrics utilize the same code.
- In this setting the schema is somewhat known, so the `apm` module engages in metadata manipulation (error ratios are calculated using the `sf_error` dimension, and the dimensions `sf_environment`, `sf_service`, `sf_operation` are assumed present throughout), whereas the more generic modules do not. Similarly, rollups are specified since the metric types are known.


#### Terminology

The `apm` module uses terminology consistent with the Splunk Infrastructure Monitoring (fka SignalFx) UI ("Sudden Change" and "Historical Anomaly") at the expense of some consistency within the library itself (e.g., [against_recent](../against_recent) is qualitatively similar to [sudden_change](latency/sudden_change)).

The `apm` module contains functions for "Static Threshold" detectors, whereas the UI handles these for usual "Infrastructure" detectors. In addition to hiding some of the metric and metadata complexity, this enables clear conditions and compound conditions to be more easily exposed.


#### Other percentiles

Splunk APM reports various percentiles as metrics. One can form estimates of other percentiles via weighted averages of the reported percentiles. Since latency distributions are often closer to log-uniform than uniform, it is advisable to use the (weighted) geometric rather than the arithmetic mean, especially for percentiles above 90 (presumably the main ones of interest). For example, to estimate the 95th percentile, one can use the following.

```
p90 = data('spans.duration.ns.p90')
p99 = data('spans.duration.ns.p99')

est_p95 = (pow(p90, 4/9) * pow(p99, 5/9)).publish('estimated_p95')
```



Note that the same logic could be applied in a scenario in which `p90` and `p99` are themselves the results of some computations (e.g., aggregating and/or transforming the input metrics).


#### Usage note

The "v2" modules (for example, [latency](latency/static_v2) and [errors](errors/static_v2)) are officially supported as part of the Splunk APM product, whereas the modules associated with "SignalFx Microservices APM PG" (the parallel [latency](latency/static) and [errors](errors/static), for example) are considered deprecated.