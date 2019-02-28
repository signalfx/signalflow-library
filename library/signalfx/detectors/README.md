The SignalFlow Library is a collection of SignalFlow modules, each of which captures a common analytical pattern used in alerting. The core of a typical module is a function which takes a required stream (signal) argument and some parameters (percent of duration, number of standard deviations, etc.) and outputs a detector. A representative use is as follows:

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

# use default values
against_recent.detector_percentile(service_cpu).publish('cpu_detector')

against_recent.detector_percentile(service_cpu, current_window=duration('3m'),
  historical_window=duration('2h'), fire_percentile_threshold=95, clear_percentile_threshold=85,
  orientation='out_of_band').publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~

Explanations of parameters and example usages can be found in the README file of each directory.

Most modules also expose streams and conditions, intermediate objects used by the corresponding detector. This facilitates the creation of statistical thresholds, as in the following example.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_periods import streams

s = data('cpu.utilization').mean()

day_baseline = streams.n_period_trimmed_mean(s, duration('10m'), duration('1d'), 6)[2]
week_baseline = streams.n_period_trimmed_mean(s, duration('30m'), duration('1w'), 2)[2]

threshold = 1.2 * max(day_baseline, week_baseline)

detect(s.mean(over='20m') > threshold).publish()
~~~~~~~~~~~~~~~~~~~~

One can also produce custom alerting conditions.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.population_comparison import conditions

s = data('cpu.utilization')

fire_, clear_ = conditions.growth_rate(s)

fire_condition = when(s > 20, '5m') or fire_
clear_condition = when(s < 18, '3m') and clear_

detect(fire_condition, clear_condition).publish()
~~~~~~~~~~~~~~~~~~~~


Most of the functions in the library can also be accessed via the SignalFx UI. The following table maps the directories in this repository to the Alert Conditions in the UI.

|Repository name|UI name|
|:---|:---|
|[not_reporting](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/not_reporting)|[Heartbeat Check](https://docs.signalfx.com/en/latest/detect-alert/alert-condition-reference/heartbeat-check.html)|
|[countdown](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/countdown)|[Resource Running Out](https://docs.signalfx.com/en/latest/detect-alert/alert-condition-reference/resource-running-out.html)|
|[population_comparison](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/population_comparison)|[Outlier Detection](https://docs.signalfx.com/en/latest/detect-alert/alert-condition-reference/outlier-detection.html)|
|[against_recent](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/against_recent)|[Sudden Change](https://docs.signalfx.com/en/latest/detect-alert/alert-condition-reference/sudden-change.html)|
|[against_periods](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/against_periods)|[Historical Anomaly](https://docs.signalfx.com/en/latest/detect-alert/alert-condition-reference/hist-anomaly.html)|
|[aperiodic](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/aperiodic)|*not available*|
|[multivariate](https://github.com/signalfx/signalflow-library/tree/master/library/signalfx/detectors/multivariate)|*not available*|
