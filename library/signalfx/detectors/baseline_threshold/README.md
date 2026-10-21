The `baseline_threshold` module detects when a signal departs from a baseline built from its own recent history. The baseline is the mean of the signal over the last several daily timeshifts (by default the same clock-time one, two, ..., seven days ago), capturing the typical daily level of the signal. Two thresholds (an upper and a lower one) are then derived from that baseline and the current value of the signal is compared against them.

The baseline is always computed over a `7d` historical period sampled once per `1d` interval.

## Detector

The `detector` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|stream|data being monitored|*None*|
|trigger_type|string|how thresholds are derived from the baseline, one of 'stddev', 'percentage'|'stddev'|
|orientation|string|specifies when the detector fires, one of 'above', 'below', 'out_of_band'|'above'|
|fire_num_stddev|number|number of sample standard deviations from the baseline required to fire; used when `trigger_type='stddev'`|2|
|clear_num_stddev|number|number of sample standard deviations from the baseline required to clear; used when `trigger_type='stddev'`|1|
|fire_percentage|number|fraction of the baseline (e.g. 0.2 == 20%) required to fire; used when `trigger_type='percentage'`|0.2|
|clear_percentage|number|fraction of the baseline (e.g. 0.1 == 10%) required to clear; used when `trigger_type='percentage'`|0.1|
|auto_resolve_after|duration|if provided, duration after which to clear when the group drops from the schema or has value None|None|
|fire_lasting|lasting|if provided, the duration/fraction for which the fire condition must hold before firing|None|

It returns a detect block that triggers when the current value of `stream` departs from its baseline. The baseline is the mean of the signal across the previous 7 days (sampled at the same clock time each day). The upper and lower thresholds are placed around the baseline either `fire_num_stddev`/`clear_num_stddev` sample standard deviations away (`trigger_type='stddev'`) or `fire_percentage`/`clear_percentage` of the baseline away (`trigger_type='percentage'`).

The `orientation` controls which thresholds matter and in which direction:

- `above` — fires when the signal rises above the upper fire threshold and clears when it falls back below the upper clear threshold.
- `below` — fires when the signal drops below the lower fire threshold and clears when it rises back above the lower clear threshold.
- `out_of_band` — fires when the signal leaves the band `[lower fire threshold, upper fire threshold]` and clears when it returns inside the band `[lower clear threshold, upper clear threshold]`.

As with the other detectors in this library the firing and clearing thresholds differ, to reduce flappiness. The fire threshold is further from the baseline than the clear threshold, so `fire_num_stddev >= clear_num_stddev` (resp. `fire_percentage >= clear_percentage`).

In `percentage` mode the threshold distances are a fraction of the baseline, so when the baseline is at (or near) zero the band collapses onto the baseline and the detector loses its hysteresis — any non-zero departure fires. `percentage` mode is therefore not suitable for signals whose baseline is expected to be zero or near zero (e.g. error counts, sparse or idle metrics, or deltas that average around zero); prefer `stddev` mode, or an absolute static threshold, for those signals.

#### Example usage

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.baseline_threshold import baseline_threshold

service_cpu = data('cpu.utilization').mean(by=['aws_tag_service'])

baseline_threshold.detector(service_cpu).publish('cpu_detector') # uses default values

# fire when cpu is more than 20% above its 7-day baseline
baseline_threshold.detector(service_cpu, trigger_type='percentage',
  fire_percentage=0.20, clear_percentage=0.1).publish('cpu_growth_detector')

# fire when cpu leaves a +/- 2 stddev band around its baseline
baseline_threshold.detector(service_cpu, orientation='out_of_band',
  fire_num_stddev=2, clear_num_stddev=1).publish('cpu_band_detector')
~~~~~~~~~~~~~~~~~~~~

#### Streams

The baseline and the thresholds are available directly from the `streams` module.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.baseline_threshold import streams

s = data('cpu.utilization').mean()

baseline, baseline_stddev = streams.baseline_stats(s)

fire_bot, clear_bot, clear_top, fire_top = streams.stddev_thresholds(baseline,
  baseline_stddev, 2, 1)
detect(s > fire_top, s < clear_top).publish()
~~~~~~~~~~~~~~~~~~~~
