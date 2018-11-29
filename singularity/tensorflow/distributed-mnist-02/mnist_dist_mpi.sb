#!/bin/bash

#SBATCH --account=ddp315
#SBATCH --partition=gpu
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=1
#SBATCH --time 00:10:00
#SBATCH --export=ALL
#SBATCH --no-requeue
#SBATCH --job-name="tensorflow-mpi-gpu"
#SBATCH --output="tensorflow-mpi-gpu.o%j.%N"
#SBATCH --gres=gpu:k80:4

declare -xr LOCAL_SCRATCH="/scratch/${USER}/${SLURM_JOB_ID}"
declare -xr LUSTRE_SCRATCH="/home/dmu/SCRATCH/SINGULARITY/images"
declare -xr SINGULARITY_MODULE='singularity/2.5.2'

module purge
module load gnu
module load mvapich2_ib
# module load openmpi_ib
module load cmake
module load "${SINGULARITY_MODULE}"
module list

rm -f host

node_list=($(scontrol show hostnames))

echo ${node_list[0]} >> host
echo ${node_list[1]} >> host
echo ${node_list[2]} >> host

export PS_HOSTS=$(singularity exec /home/dmu/SCRATCH/SINGULARITY/images/tensorflow-v1.11-gpu-20181116-mpich.simg python3 /home/dmu/SCRATCH/SINGULARITY/Distributed-TensorFlow-Using-MPI/cluster_specs.py --hosts_file=host --num_ps_hosts=1 | cut -f1 -d ' ')
export WORKER_HOSTS=$(singularity exec /home/dmu/SCRATCH/SINGULARITY/images/tensorflow-v1.11-gpu-20181116-mpich.simg python3 /home/dmu/SCRATCH/SINGULARITY/Distributed-TensorFlow-Using-MPI/cluster_specs.py --hosts_file=host --num_ps_hosts=1 | cut -f2 -d ' ')

echo $PS_HOSTS
echo $WORKER_HOSTS

mpirun -n 3 singularity exec --nv /home/dmu/SCRATCH/SINGULARITY/images/tensorflow-v1.11-gpu-20181116-mpich.simg python3 -u /home/dmu/SCRATCH/SINGULARITY/Distributed-TensorFlow-Using-MPI/cluster_dispatch.py --ps_hosts=$PS_HOSTS --worker_hosts=$WORKER_HOSTS --script=/home/dmu/SCRATCH/SINGULARITY/Distributed-TensorFlow-Using-MPI/example.py
