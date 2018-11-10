#!/bin/bash

#SBATCH --account=ddp315
#SBATCH --partition=gpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time 00:30:00
#SBATCH --export=ALL
#SBATCH --no-requeue
#SBATCH --job-name="pytorch-mnist-dist"
#SBATCH --output="pytorch-mnist-dist.o%j.%N"
#SBATCH --error="pytorch-mnist-dist.e%j.%N"
#SBATCH --gres=gpu:k80:4

declare -xr LOCAL_SCRATCH="/scratch/${USER}/${SLURM_JOB_ID}"
declare -xr LUSTRE_SCRATCH="/oasis/scratch/comet/mkandes/temp_project/singularity/images"
declare -xr SINGULARITY_MODULE='singularity/2.5.2'

module purge
module load gnu
module load mvapich2_ib
module load cmake
module load "${SINGULARITY_MODULE}"
module list

cp -rf ../../../comet-benchmark "${LOCAL_SCRATCH}"
cp "${LUSTRE_SCRATCH}/pytorch-cpu.img" "${LOCAL_SCRATCH}"

cd "${LOCAL_SCRATCH}/comet-benchmark/singularity/pytorch"

echo $(pwd)

time -p srun singularity exec --nv ${LOCAL_SCRATCH}/pytorch-cpu.img /opt/miniconda3/bin/python3 ./cpu-multi-mnist.py
