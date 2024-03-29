The `not_reporting` module contains one function. This function detects when a stream stops reporting. The SignalFx UI refers to this module as Heartbeat Check.

The `detector` function has the following parameters. Parameters with no default value are required.                         

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|stream|data stream|assumed to be decreasing|*None*|
|resource_identifier|string or list of strings|groupBy identifying the unit to monitor; None corresponds to no aggregation|None|
|duration|duration|alert when stopped reporting for this long|duration('15m')|
|auto_resolve_after|duration|if provided, duration after which to clear when group drops from schema; see Usage note below|None|

It returns a detect block that triggers when `stream` has stopped reporting for `duration`. When `resource_identifier` has the value `None`, this detector will monitor all the members of `stream` independently. When `resource_identifier` has another value, e.g. 'az', this detector will trigger (for some value, say 'west', of 'az') when *all* members of `stream` having the dimension or property 'az':'west' have stopped reporting for `duration`. The detector clears when reporting resumes.
   
#### Example usage
~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.not_reporting import not_reporting

not_reporting.detector(data('memory.utilization')).publish('memory_stopped_reporting')
~~~~~~~~~~~~~~~~~~~~

#### Condition

The condition of no longer reporting is also exposed, and can be combined with other conditions.

~~~~~~~~~~~~~~~~~~~~
from signalfx.detectors.not_reporting import conditions

s = data('memory.utilization')

mem_stopped_reporting = conditions.condition(s)
mem_too_high = when(s.fill() > 90, '12m')

detect(mem_stopped_reporting or mem_too_high).publish()
~~~~~~~~~~~~~~~~~~~~

#### Usage note

The behavior of `auto_resolve_after` may feel slightly different in this context relative to other alert conditions since the triggering condition itself involves "no data." The aspect of `auto_resolve_after` in effect here is that when a group drops from the schema (the result of some underlying time series being considered inactive), any alerts pertaining to it will be cleared by the `auto_resolve_after` mechanism. Clearing of `not_reporting` alerts within the activity period may be obtained by the use of a composite condition. An example is below.

```
A = data('heartbeat_metric')

# fires when no data for 10m, clears 30m later OR when data re-appears
detect(when(A is None, '10m') and not when(A is None, '40m')).publish('heartbeat_with_clear')
```


