# pytorch test package

### cpu tests

1. cpu-multi-mnist.py
    
    * mnist dataset
    * multiple cpus
    * tcp backend

2. run-mnist-multi-cpus.sb

    * copy "pytorch-cpu.img" to local scratch
    * run 8 cpu cores from 2 nodes

### gpu tests

1. gpu-multi-mnist.py

    * mnist dataset
    * multiple gpus
    * gloo backend
    
2. run-mnist-multi-gpus.sb

    * copy "pytorch-gpu.img" to local scratch
    * run 8 gpu cards from 2 nodes
