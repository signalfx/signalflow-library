The SignalFlow Library is a collection of SignalFlow functions, each of which captures a common analytical pattern used in alerting. For the most part, each function takes a required stream (signal) argument and some parameters (e.g. a percent of duration) and outputs a detector. A representative use is as follows:

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
