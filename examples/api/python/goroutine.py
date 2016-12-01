#!/usr/bin/env python2.7
#
# This program will watch for the metric num_goroutine to go above the
# specified threshold and start taking snapshots of goroutines and netstat
# dumps for each host that exceeds the limit every time we get another
# datapoint till the metric goes back below the threshold and then exit
#
# running it would look something like this: 
# ./goroutine.py -t TOKEN -r 1050 -s ".signalfx.com" -u mwp -d sf_source

import argparse
import requests
import signalfx
import subprocess
import threading

program = """
ingests = filter('%s', 'signalboost-ingest*')
goroutines = data('num_goroutine', filter=ingests)
detect(goroutines > %s).publish('goroutines_too_high')
"""

parser = argparse.ArgumentParser(description="snapshot golang process")
parser.add_argument("-t", "--token", required=True, help="API Access Token")
parser.add_argument("-r", "--threshold", required=True,
                    help="start recording above this value")
parser.add_argument("-o", "--output_dir", default="/tmp",
                    help="directory to put results")
parser.add_argument("-u", "--user", default="root", help="username to ssh to")
parser.add_argument("-d", "--dimension", default="hostname",
                    help="dimension on metricf that contains the hostname")
parser.add_argument("-s", "--suffix", default="",
                    help="suffix to add to the dimension to make an fqdn")

args = parser.parse_args()

flow = signalfx.SignalFx().signalflow(args.token)

program %= (args.dimension, args.threshold)


def dump_goroutines(param, state):
    r = requests.get(
        'http://{0}{1}:6060/debug/pprof/goroutine?debug=1'
        ''.format(param, args.suffix))
    with open('{0}/{1}-{2}.txt'.format(args.output_dir, param, state),
              'w') as f:
        f.write(r.text)


def dump_netstat(param, state):
    ret = subprocess.Popen(
        ["ssh", "-o StrictHostKeyChecking=no",
         "root@{0}{1}".format(param, args.suffix), "netstat -tan"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = ret.communicate()
    with open('{0}/{1}-{2}.ssh.out'.format(args.output_dir, param, state),
              'w') as f:
        f.write(out)
    with open('{0}/{1}-{2}.ssh.err'.format(args.output_dir, param, state),
              'w') as f:
        f.write(err)


threads = []


def threadit(target, args):
    t = threading.Thread(target=target, args=args)
    t.start()
    threads.append(t)


try:
    print('Executing {0} ...'.format(program))
    computation = flow.execute(program)
    state = {}
    i = 0
    for msg in computation.stream():
        if i > 0 and not state:
            print "finished"
            break
        if isinstance(msg, signalfx.signalflow.messages.DataMessage):
            for k, v in state.items():
                print('midway goroutines {0} {1}'.format(k, i))
                threadit(dump_goroutines, (k, "mid%d" % i))
                threadit(dump_netstat, (k, "mid%d" % i))
                i += 1
            pass
        if isinstance(msg, signalfx.signalflow.messages.EventMessage):
            is_state = msg.properties.get('is')
            if is_state == 'anomalous':
                inputSources = msg.properties["inputs"]
                for k, v in inputSources.items():
                    source = v["key"][args.dimension]
                    value = v["value"]
                    print('excessive goroutines {0} {1}'.format(source, value))
                    threadit(dump_goroutines, (source, is_state))
                    threadit(dump_netstat, (source, is_state))
                    state[source] = True
            if is_state == 'ok':
                inputSources = msg.properties["inputs"]
                for k, v in inputSources.items():
                    source = v["key"][args.dimension]
                    value = v["value"]
                    print('back to normal {0} {1}'.format(source, value))
                    threadit(dump_goroutines, (source, is_state))
                    threadit(dump_netstat, (source, is_state))
                    del (state[source])

    for t in threads:
        t.join()
finally:
    flow.close()
