#!/bin/bash

echo $1
echo $2
mpirun  --allow-run-as-root -np 32 --hostfile $1 \
  --report-bindings  \
  python3.8 /competition/replace_solver.py /competition/cvc5 $3

