#!/bin/bash

mpirun --allow-run-as-root -np $2 --hostfile $1 \
  python3.8 /competition/replace_solver.py 