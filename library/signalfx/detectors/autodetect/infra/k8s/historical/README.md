'Historical' detectors alert when the number of some k8s resource (within a specific cluster and namespace) in an unwanted state increased with respect to historical values.

## Resource (deployment, statefulset or daemonset) not a spec

The resource not at spec detector triggers when the number of deployments / statefulsets / daemonsets not at spec within a specific cluster and namespace increased with respect to historical values for at least 80% of the last 15 minutes. 

A deployment is not at spec when its number of available pods is not equal to the desired number of pods.

A statefulset is not at spec when its number of ready pods is not equal to the desired number of pods. Note that the granular implementation function `statefulset_pods_not_at_spec_detector` compares current pods to desired pods. Although this should work following the k8s definition of the 'current', 'ready' and 'desired' pods for a replicaset, in particular that any pod that is ready is also current (i.e. it exists), this is not the case for our metrics; there are instances were the number of current pods is 0, even though there are multiple ready pods. To bypass this issue, the statefulset not at spec scoped implementation relies on the number of ready pods instead.

A daemonset is not at spec when its number of ready nodes is not equal to the desired number of scheduled nodes.

The alert is cleared when the number of deployments / statefulsets / daemonsets not at spec has dropped below the alert level for at least 90% of the last 40 minutes.

Parameters:
- `guard: float = 0` minimum number of deployments / statefulsets / daemonsets not at spec to alert for.
- `headroom: float = 1` how much worse the number of deployments / statefulsetes / daemonsets not at spec must be, compared to historical data, to trigger an alert.
- `filter_: filter = None` dimensional scope for the detector, e.g. `filter('k8s.cluster.name', 'us1')`
