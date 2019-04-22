#!/bin/bash
##SBATCH -N 1        # Ensure that all cores are on one machine
#SBATCH -n 512      # Number of cores
#SBATCH -t 1-00:00  # Runtime in d-hh:mm
#SBATCH -p shared   # Partition to submit to
#SBATCH --reservation=ac290r
#SBATCH --mem-per-cpu=4000
##SBATCH -o job_%j.out
##SBATCH -e job_%j.err

#module load intel/15.0.0-fasrc01 openmpi/1.10.0-fasrc01
#module load MYPROGRAM

# module load gcc/8.2.0-fasrc01 openmpi/3.1.1-fasrc01 cuda/10.0.130-fasrc01
module load gcc/7.1.0-fasrc01 openmpi/3.1.1-fasrc01 cuda/10.0.130-fasrc01

srun -n $SLURM_NTASKS --mpi=pmi2 ./run2.py > out.txt 2> err.txt
