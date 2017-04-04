The signalflow-library is a collection of signalflow programs, each of which captures a common analytical pattern used in alerting. For the most part, each function takes a required stream (signal) argument and some parameters (e.g. a percent of duration) and outputs a detector. A representative use is as follows:

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.against_recent import against_recent

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

against_recent.detector_percentile(service_cpu).publish('cpu_detector') # uses default values

against_recent.detector_percentile(service_cpu, current_window=duration('3m'),
  historical_window=duration('2h'), fire_percentile_threshold=95, clear_percentile_threshold=85,
  orientation='out_of_band').publish('custom_cpu_detector')
~~~~~~~~~~~~~~~~~~~~

Explanations of parameters and example usages can be found in the README file of each subdirectory of this directory.


The functions in the library can also be accessed via the SignalFx UI. The following table maps the directories in this repository to the Alert Conditions in the UI.

|repository name|UI name|
|---|---|
|not_reporting|Heartbeat Check|
|countdown|Resource Running Out|
|population_comparison|Outlier Detection|
|against_recent|Sudden Change|
|against_periods|Historical Anomaly|
|aperiodic|*not available*|
|multivariate|*not available*|
|advanced|*not available*|
