The `apm` module consists primarily of the submodules `errors` and `latency`.


#### Differences with the rest of the SignalFlow Library

The functions in the `apm` module operate on metrics with a known meaning and metadata. As a consequence, it is possible to develop somewhat tailored alerting strategies.

Some of the principal differences are as follows:

- Whereas the functions appearing in `against_recent`, `against_periods`, `aperiodic`, `countdown`, and `not_reporting` generally take an input stream as an argument, the functions in the `apm` module do not take input streams. Rather, they take filters and other parameters, and these produce data blocks that are passed to statistically-oriented procedures.
- Since the APM metrics consist of percentiles and counts, the patterns do not have the same general applicability as those captured in the modules mentioned above. For example, an estimate of the spread of a distribution can be obtained by taking the difference between percentiles, and an alert can be conditioned on the volume of traffic (captured in the metric `spans.count`) via a compound condition. Of course, the patterns do apply to other scenarios in which percentiles are emitted as metrics (replacing the metrics `spans.duration.ns.*` and `spans.count` as appropriate).
- In this setting the schema is somewhat known, so the `apm` module engages in metadata manipulation (error rates are calculated using the `error` dimension, and the dimensions `cluster`, `service`, `operation` are assumed present throughout), whereas the other modules do not. Similarly, rollups are specified since the metric types are known.


#### Terminology

The `apm` module uses terminology consistent with the SignalFx UI ("Sudden Change" and "Historical Anomaly") at the expense of some consistency within the library itself (e.g., `against_recent` is qualitatively similar to `apm/latency/sudden_change`).

The `apm` module contains functions for "Static Threshold" detectors, whereas the SignalFx UI handles these for usual "Infrastructure" detectors.
