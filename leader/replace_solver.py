#!/usr/bin/env python3
import json
import logging
import os
import subprocess
import sys
from mpi4py import MPI
from solver_utils import *

'''
NOTE: Need to make the solver script call this one, I think.
'''

comm_world = MPI.COMM_WORLD
my_rank = comm_world.Get_rank()
num_procs = comm_world.Get_size()

original_input = ""
partition_file = ""

request_directory = sys.argv[1]
input_json = get_input_json(request_directory)
problem_path = input_json.get("problem_path")
#problem_path = ("/home/amalee/QF_LRA/2017-Heizmann-UltimateInvariantSynthesis"
#                "/_array_monotonic.i_3_2_2.bpl_11.smt2")

partitioner = "cvc5"
#partitioner="/home/amalee/cvc5/build/bin/cvc5"
partitioner_options = ("--append-learned-literals-to-cubes "
                       "--produce-learned-literals")
number_of_partitions = str(num_procs)
output_file = "partition_file"
smt_file = problem_path
checks_before_partition = "5000"
checks_between_partitions = "0"
strategy = "heap-trail"


# Note: should probably do a nonblocking scatter.

if (my_rank == 0):
  # partition the input
  my_partitions = make_partitions(partitioner, partitioner_options, number_of_partitions,
                                  output_file, smt_file,
                                  checks_before_partition, checks_between_partitions,
                                  strategy)
else:
  my_partitions = None

# Now scatter partitions to the workers.
# For now, num partitions = num workers.
# In fact, list slicing does not seem to be support by the
#   mpi library. Note to self - might need to do a c++ impl
#   and interface with it here so that I can have a queue.
my_partition = comm_world.scatter(my_partitions, root=0)

stitched_partition_directory = "./"

stitched_problem = stitch_partition(my_partition, my_rank, stitched_partition_directory,
                                    problem_path)

result = run_solver(partitioner, stitched_problem)


if (my_rank != 0):
  # maybe communicate the outputs from all workers to the main solver
  comm_world.send(result, dest=0, tag=99)
else:
  rank = None
  # Problem: this is blocking and waits for the longest partition.
  # May be better to monitor the logs.
  if result == "sat":
    print("found result SAT")
  else:
    for rank in range(1, num_procs):
      result = comm_world.recv(source=rank, tag=99)
      # Only one sat needs to exist for the whole problem to be sat.
      if result == "sat":
        print("found result SAT")
        break
    # TODO: return unknowns and errors properly.
    print("found result UNSAT")
