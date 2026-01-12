'Scoped' detectors alert only when the ratio of some k8s resource in an unwanted state within a cluster or namespace exceeds a specified fire threshold ratio.

## Container restarts per cluster or namespace detector

The container restarts detector triggers when the ratio of pods with the same container name within a cluster or namespace experiencing container restarts exceeds the fire threshold for at least 80% of the last 15 minutes. The container restarts per pod are summed over a period of 5 minutes. A pod is considered to experience container restarts when the number of restarts over 5 minutes is equal to or greater than 1. The alert is cleared when the ratio of pods experiencing container restarts has dropped to half the fire threshold for 100% of the last 40 minutes.

Parameters:
- `fire_threshold_: float = 0.33`
- `filter_: filter = None` specifies dimensional scope for the detector, e.g. `filter('k8s.namespace.name', 'o11y-rum')`

## Resource (deployment, statefulset or daemonset) not a spec per cluster or namespace

The resource not at spec detector triggers when the ratio of deployments / statefulsets / daemonsets not at spec within a cluster or namespace exceeds the fire threshold for at least 80% of the last 15 minutes.

A deployment is not at spec when its number of available pods is not equal to the desired number of pods.

A statefulset is not at spec when its number of ready pods is not equal to the desired number of pods. Note that the granular implementation function `statefulset_pods_not_at_spec_detector` compares current pods to desired pods. Although this should work following the k8s definition of the 'current', 'ready' and 'desired' pods for a replicaset, in particular that any pod that is ready is also current (i.e. it exists), this is not the case for our metrics; there are instances were the number of current pods is 0, even though there are multiple ready pods. To bypass this issue, the statefulset not at spec scoped implementation relies on the number of ready pods instead.

A daemonset is not at spec when its number of ready nodes is not equal to the desired number of scheduled nodes.

The alert is cleared when the ratio of deployments / statefulsets / daemonsets not at spec has dropped to half the fire threshold for at least 90% of the last 40 minutes.

Parameters:
- `fire_threshold_: float = 0.25`
- `filter_: filter = None` specifies the dimensional scope for the detector, e.g. `filter('k8s.cluster.name', 'us1')`

## Pods in failed and pending state per cluster or namespace

The pods in failed and pending state detector triggers when the ratio of pods in failed and pending state within a cluster or namespace exceeds the fire threshold for at least 80% of the last 15 minutes. The alert is cleared when the ratio drops to half the fire threshold for at least 90% of the last 40 minutes.

Parameters:
- `fire_threshold_: float = 0.33`
- `filter_: filter = None` specifies dimensional scope for the detector, e.g. `filter('k8s.namespace.name', 'o11y-rum')`

## Job failures per cluster or namespace 

The job failures detector triggers when the ratio of high-failure jobs within a cluster or namespace exceeds the fire threshold for at least 80% of the last 15 minutes. A job is considered high-failure if its ratio of failed pods exceeds the high failure job threshold. The alert is cleared when the ratio of high-failure jobs has dropped to half the fire threshold for 100% of the last 40 minutes.

Parameters:
- `high_failure_job_threshold: float = 0.9`
- `fire_threshold_: float = 0.33`
- `filter_: filter = None` specifies the dimensional scope for the detector, e.g. `filter('k8s.namespace.name', 'o11y-rum')`

## Node CPU / memory utilization per cluster detector

The node CPU / memory utilization detector triggers when more than 1% of nodes within a cluster have CPU / memory utilization:
- above 95% for at least 60% of the last 3 minutes OR
- above 90% for at least 80% of the last 8 minutes OR
- above 80% for at least 80% of the last 15 minutes


The alert is cleared when less than 1% of pods within a cluster have CPU / memory utilization:
- above 95% for at least 90% of the last 10 minutes AND
- above 90% for at least 90% of the last 15 minutes AND
- above 80% for at least 90& of the last 25 minutes

Parameters:
- `filter_: filter = None` specifies dimensional scope for the detector, e.g. `filter('k8s.cluster.name', 'us1')`

## Node readiness per cluster detector

The node readiness detector triggers when the percentage of nodes ready within a cluster is:
- less than 90% for the last minute OR
- less than 95% for at least 80% of the last 5 minutes


The alert is cleared when the percentage of nodes ready within a cluster is:
- more than 90% for the last 8 minutes AND
- more than 95% for at least 80% of the last 15 minutes

Parameters:
- `filter_: filter = None` specifies dimensional scope for the detector, e.g. `filter('kubernetes_cluster', 'us1')`
