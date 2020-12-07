The `quantiles` module enables the extraction of quantiles from histograms represented as a family of counters (or cumulative counters) each tracking the count of observations less than (or less than or equal to) some threshold. The thresholds define the bin edges of the histogram. This is a standard approximation method, and the quality of any particular application is controlled by the quality of the binning (better for observations to be spread among the bins than concentrated in a few bins) and, since we use linear interpolation within the bins, the degree to which the assumption of uniformity within each bin holds.

The `histogram` submodule contains two functions. The `quantile` function returns a stream object which computes a specified quantile of a specified metric, given the binning information. Additional filtering and aggregation (across both dimensions/properties, and time) may be incorporated as well. The `percentile` function is nearly identical, except the desired rank is expressed in the range 0 to 100 rather than the range 0 to 1.

The `quantile` function has the following parameters. Parameters with no default value are required. The `percentile` function differs only in the assumed scale of the second argument.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|metric_name|string|name of metric of which a quantile is desired|*None*|
|target_quantile|number|desired quantile (between 0 and 1, inclusive)|*None*|
|bin_edges|list of numbers|histogram bin edges, in ascending order|*None*|
|bin_edges_as_str|list of strings|string version of `bin_edges`; if provided, length must agree with that of `bin_edges`|default `None` will apply the `str()` function to the elements of `bin_edges`|
|roll_up|string|a valid rollup string, should generally be one of 'delta', 'sum'; use 'delta' for cumulative counter, 'sum' for counter data|'delta'|
|dimension_key|string|name of dimension used to identify the metric as tracking count of observations below a threshold; typically something like 'upper_bound' or 'leq'|'upper_bound'|
|filter_|filter|additional filters to apply|default `None` does no additional filtering|
|group_by|string or list of strings|additional dimensions/properties by which to group the calculation|default `None` does no grouping|
|window|duration or string|window over which to calculate|default `None` will calculate one timestamp at a time|
|minimum_value|number|value to use for interpolation with the first bin edge, in case the desired quantile is smaller than the first bin edge|default `None` does no interpolation and will use the smallest (i.e., first) element of `bin_edges`|


#### Example usage

In the example we assume the metric `latency_bucket` reports with dimension `upper_bound`, and the values of this dimension are `'0.001'`, `'0.01'`, `'0.1'`, `'1.0'`, and `'50.0'`.

The program publishes (an approximation of) the 99th percentile of this metric.

~~~~~~~~~~~~~~~~~~~~
from signalfx.stats.quantiles import histogram

c = [0.001, 0.01, 0.1, 1.0, 50.0]
histogram.quantile('latency_bucket', 0.99, c).publish('P99')
~~~~~~~~~~~~~~~~~~~~

#### Usage notes

The items in `bin_edges` are used to perform the interpolation, and those of `bin_edges_as_str` are used to populate filters. These are exposed as separate arguments to handle possible discrepancies between dimension values (for `dimension_key`) and the result of applying `str()` to items in `bin_edges` (e.g., 0.01 represented as '0.010000').

Another application of `bin_edges_as_str` is to handle a final "infinity" bin edge. Suppose in the above example we also have a `upper_bound:+Inf` dimension, and wish to interpolate from 50 to 1000 if the P99 lies above 50. This can be achieved as follows:

~~~~~~~~~~~~~~~~~~~~
from signalfx.stats.quantiles import histogram

c = [0.001, 0.01, 0.1, 1.0, 50.0]
c_infty = c + [1000]
c_infty_str = [str(x) for x in c] + ['+Inf']

histogram.quantile('latency_bucket', 0.99, c_infty, bin_edges_as_str=c_infty_str).publish('P99')
~~~~~~~~~~~~~~~~~~~~

To perform no additional interpolation, i.e., to simply use the value 50 (when the desired quantile lies above 50), one would use instead `c_infty = c + [50]` in the immediately preceding program.

Some annoyances are present in the first bin as well. In this case the desired quantile can be computed using interpolation against a supplied value (`minimum_value`) when the desired quantile is smaller than the first bin edge; by default no additional interpolation is performed and the quantile will be computed as the first bin edge.

The dimensions/properties provided to `group_by` are used to aggregate, but their presence is not required (i.e., `allow_missing` is utilized). Consequently, a full aggregation can be obtained by providing to `group_by` a string which is not present as a dimension/property on the data (e.g., a nonsense string).