#!/bin/bash
#SBATCH --mail-type=END,FAIL

## NOTE: %u=userID, %x=jobName, %N=nodeID, %j=jobID, %A=arrayID, %a=arrayTaskID
#SBATCH --output=/mnt/research/d.byrd/students/rdasgupt/poker-goat/output/RunModel%j.out  # Output file
#SBATCH --error=/mnt/research/d.byrd/students/rdasgupt/poker-goat/output/RunModelError%j.err   # Error file
#SBATCH --mem=100G                  # Memory reservation
#SBATCH -n 10                        # CPU reservation

# Use this (with 1 CPU and 100 GB RAM)...
python3 game/pokerGame.py 5