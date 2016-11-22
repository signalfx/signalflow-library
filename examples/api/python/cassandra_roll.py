#!/bin/env python
#
# cassandra_roll.py <token> [<filter_str>]
#
# Watches for hinted handoff of a cassandra cluster to go back down to 0
# after a node in a cassandra cluster is restarted. filter_str is an
# optional signalflow filter expression e.g filter('cluster', 'my_cluster')
#
from __future__ import print_function
import signalfx

PROGRAM = '''
# get the data and sum it across the cluster as "hinted handoffs" will accumulate across more than one node in the cluster.
# also sum the data over 1 minute to make sure that we don't get fooled by little dips in the hinted handoffs
hinted_handoffs=data('gauge.cassandra.Storage.TotalHintsInProgress.Count', %s).sum().sum(over='1m')
not_ready = hinted_handoffs > 0
ready = when(hinted_handoffs == 0, '2m')
detect(on = not_ready, off = ready).publish('hinted_handoffs')
'''

def run(token, filter_str):
    
    flow = signalfx.SignalFx().signalflow(token)
    try:
        computation = flow.execute(PROGRAM % filter_str)
        went_anomalous = False
        for msg in computation.stream():
            if isinstance(msg, signalfx.signalflow.messages.EventMessage):
                    state = msg.properties.get('is')
                    if state == 'anomalous':
                        went_anomalous = True
                    if state == 'ok' and went_anomalous:
                        print('Handed hintoffs cleared')
                        break
    finally:
            flow.close()

if __name__ == '__main__':
    import sys
    token = sys.argv[1]
    filter_str = sys.argv[2] if len(sys.argv) == 3 else ''
    run(token, filter_str)
