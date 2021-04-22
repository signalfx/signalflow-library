## Intermediate to advanced SignalFlow

SignalFlow is the API for specifying a computation in the SignalFx (Splunk Infrastructure Monitoring) streaming analytics system. SignalFlow is a programming language whose syntax is modeled on the syntax of Python. While SignalFlow supports a sliver of Python functionality, and disagrees with Python in some cases, the SignalFlow experience is broadly “write Python, get streaming charts and alerts.”

This document describes some SignalFlow functionality which makes it easier to write, read, and maintain; and also allows for the concise expression of more complex calculations. The reader may notice many of these features are used in this library. This document is intended as a supplement to the core SignalFlow [documentation](https://dev.splunk.com/observability/docs/signalflow/); our goal is to explain high-level language concepts and some advanced features, not to provide (for example) an exhaustive list of stream methods and functions.

### Generic programming language capabilities
Here we describe functionality to support clean, concise, and reusable code (not specific to streaming calculations).
#### User-defined functions
Functions may be defined and applied in the context of a single SignalFlow program. SignalFlow function definition follows Python syntax. The contents returned by a function may be unpacked inline.
```python
def remove_trend_and_seasonality(s, season=duration('1w')):
    t = s.delta()
    return t - t.timeshift(season)
```

The body of a function may call other functions (built-in or user-defined), assign variables, and apply conditional operators (`if`, `elif`, `else`) on static values. Note that variables can be bound exactly once (e.g., `n = n + 1` is not permitted).

#### Container types: dictionaries, lists, and tuples
Various container types can be created and assigned as in Python, with the notable difference that they are immutable in SignalFlow. Dictionaries are useful for organizing the contents of a function’s return value, defining shorthand, and avoiding repetition. Dictionaries are also used to define `const()` blocks, and may be used to specify a filter in a `data()` block.

Dictionary values and list/tuple entries are accessed as in Python.
```python
# some horizontal lines
a = (1, 3, 4)
const(a[1]).publish()

d = {'a': 1, 'b': 2}
const(d['a']).publish()
```


#### More on lists
SignalFlow has a familiar built-in `range()` list constructor.

```python
# another horizontal line
lst = range(3, 10, 2)
const(lst[3]).publish()
```

List comprehensions make working with lists a bit easier.

```python
metrics = ['cpu.utilization', 'memory.utilization']
streams = [data(m) for m in metrics]
# assume function definition above appears in the program
transformed = [remove_trend_and_seasonality(s) for s in streams]
```

Lists can contain arbitrary types, making it easy to reuse the same collection of filters, metrics, constant values, etc. in the context of a single program. One can also “splat” a list in order to supply its contents as arguments to another function (built-in or user-defined).

`max(*transformed).publish()`

One can also take the `len()` of a list, and add (with `+`) two lists together.
#### Miscellaneous
**Module imports.** Currently only the modules of this (built-in) SignalFlow library are available; this repository contains many examples showing how to import, and serves also as an inventory of available modules. User-defined modules may be supported some day as well.

**Assertions.** These are boolean expressions on static values, evaluated at compile time. The main application is to check correctness of arguments supplied, more useful for libraries than single programs. Failure prevents the job from running.

**Conveniences.** `str()`, string addition, comments (as featured above); `is`, `None`.

**Arithmetic.** SignalFlow uses floating point (not integer) arithmetic since a SignalFlow client is not expected to know (and is not able to cast) the type emitted by a stream. This reflects some kind of principle of least surprise.

### Working with streams
The star of most SignalFlow shows is the stream object. This can be thought of as a time-parameterized NumPy array or pandas DataFrame. Most SignalFlow programs begin with a `data()` block (not unlike a Python script beginning with the creation of a pandas Series/DataFrame), which specifies a query that may be run against both incoming streams and historical data.

Familiar primitive operations (mean, variance, percentile, exclude, ewma, timeshift, map(lambda), …)  are available as methods and/or functions on numerical streams. Stream methods can be chained. New streams can be created by functions, including the usual arithmetic operations.

#### Boolean streams and detectors
A comparison (inequality or equality) between numerical streams (or between a numerical stream and a constant value) is a (boolean) stream in its own right. Boolean streams can be assigned like any other, and combined using the standard operations (`and`, `or`, `not`). To express that a certain condition has held for a percentage of duration, use the [when](https://dev.splunk.com/observability/docs/signalflow/functions/when_function/) function. Conceptually this can be thought of as a window transformation on boolean streams, and creates yet another boolean stream.

Boolean streams can be supplied to the [detect](https://dev.splunk.com/observability/docs/signalflow/functions/detect_function/) function, which allows for the continuous evaluation of the condition, and the creation of trigger/clear events in the SignalFx system.

It is extremely good practice to use distinct conditions for triggering and clearing an alert; if no explicit clearing condition is specified, an alert clears once the triggering condition becomes false. The main motivation is to prevent “flappy” alerts caused by a signal value hovering around a threshold: making the alert slower to clear will usually have the effect of merging a rapid succession of alert-clear’s into one logical incident. The SignalFlow library facilitates (and has as its default behavior) the use of distinct triggering and clearing conditions. Note the library exposes, in addition to the fully-formed detect blocks, companion conditions and streams modules (essentially, such modules for each alert type), which allow the user to access intermediate calculations and constructions in SignalFlow programs. Typical applications would be to take the minimum/maximum of a statistically defined threshold and a static threshold, or to combine custom alert conditions with built-in conditions based on statistical procedures (see, e.g., [here](../detectors/against_recent/README.md)). When an explicit clearing condition is used, additional flexibility is provided by the evaluation mode of the detect block (split or paired). 

Note that boolean streams can produce `True`, `False`, or `None`, and `when` conditions compare the number of `True`'s to the sum of the numbers of `True`'s, `False`'s, and `None`'s in the window when determining whether the condition has held for the specified percentage of duration. For example, `s > 5` evaluates to `None` at a timestamp for which `s` produces the value `None`. This may lead to undesirable behavior for aperiodic/sparse emitters, and the [aperiodic](../detectors/aperiodic/README.md) module is at least a partial remedy. For more control, `None` values can be handled explicitly (e.g., by extrapolation or a map). This can be done to the boolean streams themselves, e.g.:

`when(s > 5).map(lambda x: True if x is True or x is None else False)`. 

Note the following formulation allows for summing/averaging:

`when(s > 5).map(lambda x: 1 if x is True or x is None else 0)`.

#### Conditional operators on streams
While conditional operators on streams may not be used to manage the control flow of a function, there is an `if-else` stream constructor that may be used to perform more complex filtering operations and to build more complex calculations. For streams `s` and `t` and a boolean stream `b`, a new stream may be defined as `s if b else t`.  The boolean stream `b` may be defined via the `when` function, or by an inequality (say) defined inline. Note that metadata correlation is applied to the triple `s, b, t` (just as it applies when computing the schema of an expression such as `s + t`).

The following is an example application. (The correlation coefficient is provided by this [library](../detectors/multivariate/correlation.flow) but is included here for expositional reasons.)

```python
def correlation_coefficient(s1, s2, d=duration('1h')):
    # calculates correlation coefficient of s1 and s2 over d
    b = s1 is not None and s2 is not None
    s_1 = s1 if b else None
    s_2 = s2 if b else None
    p = s_1.mean(over=d) * s_2.mean(over=d)
    cov = (s_1 * s_2).mean(over=d) - p
    return cov / (s_1.stddev(over=d) * s_2.stddev(over=d))

t = … # some target series (want to be correlated with)
s = … # stream whose members will be compared to t
filtered_s = s if correlation_coefficient(s, t) > 0.8 else None
filtered_s.publish()
```

#### Specifying resolution in a `data()` block
It is possible to set the resolution in a `data()` block (using the keyword argument `resolution`, in milliseconds). For time series with a resolution (regular spacing between datapoints), using this is not recommended: SignalFx will estimate the resolution for you. For aperiodic data (generally event-driven), or data with known but coarse resolution plus some other pathological property, setting the resolution in the `data()` block may help. The resolution should always be a multiple of 1000 (i.e., one second). There are two general scenarios:
- You know the resolution, but for sparsity-type reasons, SignalFx does not discover the “correct” resolution every time (since different data may be available depending on when the job is started). This can happen for low-resolution (e.g., 5-minute) metrics.
- There is no resolution (you essentially have event data), and you want to be guaranteed that certain calculations (involving timeshifts, windows, or calculating time elapsed) make sense. For example, if the program queries several 3-minute windows over the last hour and combines them in some interesting way, running this calculation at 2-hour resolution will be hard to reason about.

Note the resulting time series will typically have many null values, and these need to be handled (by extrapolation/fill/map, applying a window transformation, if-else constructor handling None, or the aperiodic module). Also note (as of this writing) a SignalFx job (computation) has a single resolution, determined in a two-step process: analysis of the resolution of the input time series, followed by possible coarsening due to arguments in the program (long transformation windows, timeshifts resulting in retrieval of older data for which only a coarser resolution is available). Setting the resolution in a `data()` block sidesteps the first step of this process, but not the second, so the job (detector/chart) may run at a resolution coarser than specified. (It cannot run at a finer resolution).

#### Miscellaneous
Arithmetic on durations (addition of durations, multiplication of durations by scalars) is supported. This can be used to retrieve multiple timeshifts of a stream `s` with, for example:

`[s.timeshift(i * duration('1d')).publish('shift_' + str(i) + '_d') for i in range(1, 4)]`

Note we could pass this list (splatted) to a statistical function.

### Putting it all together
We express somewhat involved streaming calculations without writing too much code.
#### Working with histograms
In this example, assuming we implement a histogram by emitting counts of values less than or equal to certain “cut points” (knowledge shared between the instrumentation and the SignalFlow client), and model these as dimensions, we use linear interpolation to estimate a given quantile. This estimation has the good property that its accuracy is determined by the quality of the binning and the degree to which the uniformity within bins assumption holds, but is not sensitive to the window over which the quantile is calculated per se. (Beware quantiles landing in the first or last bin.) Note a more robust version is now captured in this [library](../stats/quantiles/histogram.flow), so is included here as an illustration.

```python
CUT_POINTS = range(10, 110, 10)

# assume thresholds are expressed as dimensions with key 'leq'
filters = [filter('leq', str(cut_point)) for cut_point in CUT_POINTS]

metric_name = 'my_metric'
target_percentile = 95

#  rollup='sum' for counters, rollup='delta' for cumulative counters
cdf = [data(metric_name, rollup='sum', extrapolation='zero', filter=f) for f in filters]

# for calculations over windows, use instead:
cdf = [data(metric_name, rollup='sum', extrapolation='zero', filter=f).sum(over='1d') for f in filters]

data_target = cdf[len(CUT_POINTS) - 1] * target_percentile / 100.0

above_ = [(data_target - cdf[i]) / (cdf[i + 1] - cdf[i]) * (CUT_POINTS[i + 1] - CUT_POINTS[i]) + CUT_POINTS[i] if data_target >= cdf[i] and data_target < cdf[i+1] else 0 for i in range(len(CUT_POINTS) - 1)]

sum(*[x.fill(0) for x in above_]).publish('estimated_' + str(target_percentile) + '_percentile')
```

#### Working with distributions
In this example, we estimate the relative entropy between a stream (thought of as a distribution) and a smoothed and timeshifted form of the same stream. The estimate is influenced by the quality of the cut points chosen; this could be improved by computing proportions of one stream relative to some percentiles of the other. In any case, this gives a way of comparing the current population distribution to a historical baseline distribution.

```python
d = … # stream, decently-sized population of emitters
CUT_POINTS = range(0, 110, 10)

def stream_to_proportions(s, cut_points=CUT_POINTS):
   return [(1 if s > cut_points[i-1] and s <= cut_points[i] else None).count() / s.count() for i in range(1, len(cut_points))]

def relative_entropy(p, q):
   assert len(p) == len(q)
   return - sum(*[p[i] * ((q[i] / p[i]).log() if p[i] > 0 else 0) for i in range(len(p))])

a = stream_to_proportions(d)

# can adjust how the prior is defined
b = stream_to_proportions(d.timeshift('1d').mean(over='3h')) 

relative_entropy(a, b).publish('KL')
```