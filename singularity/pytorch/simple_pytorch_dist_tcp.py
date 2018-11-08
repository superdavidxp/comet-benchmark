#!/usr/bin/env python
import os
import socket
import torch
import torch.distributed as dist
from mpi4py import MPI


def run(rank, size, host, ipad):
    """ Distributed function to be implemented later. """
    print("|    I am rank {} in {} at {} :: {}".format(rank, size, host, ipad))
    pass


def init_processes(rank, size, host, ipad, fn, backend='tcp'):
    """ Initialize the distributed environment. """
    os.environ['MASTER_ADDR'] = ipad
    os.environ['MASTER_PORT'] = '29500'
    dist.init_process_group(backend, rank=rank, world_size=size)
    fn(rank, size, host, ipad)


if __name__ == "__main__":

    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    host = socket.gethostname()
    ipad = socket.gethostbyname(host)

    init_processes(rank, size, host, ipad, run)

    MPI.COMM_WORLD.Barrier()
    MPI.Finalize()
