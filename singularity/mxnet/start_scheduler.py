import os
import argparse

parser = argparse.ArgumentParser(description='distributed mxnet scheduler')
parser.add_argument('--ps-root-uri', default='127.0.0.1', metavar='127.0.0.1', help='mxnet scheduler ip address (default: 127.0.0.1)')
parser.add_argument('--ps-root-port', type=int, default=9000, metavar='N', help='mxnet scheduler port number (default: 9000)')
parser.add_argument('--ps-verbose', type=int, default=1, metavar='N', help='mxnet scheduler mode (default: 1)')
parser.add_argument('--num-server', type=int, default=1, metavar='N', help='number of server (default: 1)')
parser.add_argument('--num-worker', type=int, default=2, metavar='N', help='number of worker (default: 2)')

args = parser.parse_args()

os.environ.update({
  "DMLC_ROLE": "scheduler", # Could be "scheduler", "worker" or "server"
  "DMLC_PS_ROOT_URI": args.ps_root_uri, # IP address of a scheduler
  "DMLC_PS_ROOT_PORT": str(args.ps_root_port), # Port of a scheduler
  "DMLC_NUM_SERVER": str(args.num_server), # Number of servers in cluster
  "DMLC_NUM_WORKER": str(args.num_worker), # Number of workers in cluster
  "PS_VERBOSE": str(args.ps_verbose) # Debug mode
})

import mxnet as mx
