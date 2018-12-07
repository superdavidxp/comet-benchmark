import socket
import os
import time
import logging
import subprocess
import mxnet as mx
import numpy as np
from sklearn.model_selection import train_test_split
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

hostname = socket.gethostname()

output = subprocess.check_output("ip addr show em1 | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/'", shell=True)
ipaddr = output.decode("utf-8")

psip = ipaddr
psip = comm.bcast(psip, root=0)

ipaddr = ipaddr.strip()
psip = psip.strip()

comm.Barrier()
print(size, rank, "ipaddr =", ipaddr, "psip =", psip)
comm.Barrier()

if rank == 0:
    # run scheduler
    os.environ.update({
        "DMLC_ROLE": "scheduler", # Could be "scheduler", "worker" or "server"
        "DMLC_PS_ROOT_URI": psip, # IP address of a scheduler
        "DMLC_PS_ROOT_PORT": "9000", # Port of a scheduler
        "DMLC_NUM_SERVER": "1", # Number of servers in cluster
        "DMLC_NUM_WORKER": "1", # Number of workers in cluster
        "PS_VERBOSE": "2" # Debug mode
    })
    print(size, rank, "ipaddr =", ipaddr, "scheduler starts !")

if rank == 1:
    # run server
    os.environ.update({
        "DMLC_ROLE": "server", # Could be "scheduler", "worker" or "server"
        "DMLC_PS_ROOT_URI": psip, # IP address of a scheduler
        "DMLC_PS_ROOT_PORT": "9000", # Port of a scheduler
        "DMLC_NUM_SERVER": "1", # Number of servers in cluster
        "DMLC_NUM_WORKER": "1", # Number of workers in cluster
        "PS_VERBOSE": "2" # Debug mode
    })
    print(size, rank, "ipaddr =", ipaddr, "server starts !")

if rank == 2:
    # run workers
    os.environ.update({
        "DMLC_ROLE": "worker",
        "DMLC_PS_ROOT_URI": psip,
        "DMLC_PS_ROOT_PORT": "9000",
        "DMLC_NUM_SERVER": "1",
        "DMLC_NUM_WORKER": "1",
        "PS_VERBOSE": "2"
    })
    print(size, rank, "ipaddr =", ipaddr, "worker starts !")

    # start worker jobs
    logging.getLogger().setLevel(logging.DEBUG)

    # lineral equation
    def f(x):
      # a = 5
      # b = 2
      return 5 * x + 2

    # Data
    X = np.arange(100, step=0.001)
    Y = f(X)

    # Split data for taining and evaluation
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
    kv_store = mx.kv.create('dist_sync')

    batch_size = 1024
    train_iter = mx.io.NDArrayIter(X_train, 
                                   Y_train, 
                                   batch_size, 
                                   shuffle=True,
                                   label_name='lin_reg_label')
    eval_iter = mx.io.NDArrayIter(X_test, 
                                  Y_test, 
                                  batch_size, 
                                  shuffle=False)

    X = mx.sym.Variable('data')
    Y = mx.symbol.Variable('lin_reg_label')
    fully_connected_layer  = mx.sym.FullyConnected(data=X, name='fc1', num_hidden = 1)
    lro = mx.sym.LinearRegressionOutput(data=fully_connected_layer, label=Y, name="lro")

    model = mx.mod.Module(
        symbol = lro ,
        data_names=['data'],
        label_names = ['lin_reg_label']# network structure
    )
    time1 = time.time()

    model.fit(train_iter, eval_iter,
                optimizer_params={
                    'learning_rate':0.000000002},
                num_epoch=20,
                eval_metric='mae',
                batch_end_callback
                     = mx.callback.Speedometer(batch_size, 20),
                kvstore=kv_store)

    time2 = time.time()
    print('training took %0.3f ms' % ((time2 - time1) * 1000.0))
