#!/usr/bin/env python3.8
import json
import logging
import os
import subprocess
import sys
from mpi4py import MPI
from solver_utils import *
from mpi4py.futures import MPICommExecutor

'''
NOTE: Need to make the solver script call this one, I think.
'''

comm_world = MPI.COMM_WORLD
my_rank = comm_world.Get_rank()
num_procs = comm_world.Get_size()

original_input = ""
partition_file = ""

##### LOCAL STUFF #####
problem_path = ("/home/amalee/QF_LRA/2017-Heizmann-UltimateInvariantSynthesis/"
                "_array_monotonic.i_3_2_2.bpl_11.smt2")
# "_fragtest_simple.i_4_5_4.bpl_7.smt2")
partitioner = "/home/amalee/cvc5/build/bin/cvc5"


##### CLOUD STUFF #####
# problem_path = sys.argv[1]
# partitioner = "./cvc5"


partitioner_options = ("--append-learned-literals-to-cubes "
                       "--produce-learned-literals")
number_of_partitions = str(num_procs - 1)
output_file = "partition_file"
smt_file = problem_path
checks_before_partition = "625"
checks_between_partitions = "625"
strategy = "strict-cube"


# Note: should probably do a nonblocking scatter.

if (my_rank == 0):
    print(f"my rank is {my_rank} and I am going to partition {problem_path}")
    # partition the input
    print(f"Hello from the partitioning node \n"
          f" partitioner {partitioner} "
          f" partitioner_options {partitioner_options}"
          f" num partitions {number_of_partitions}"
          f" output_file {output_file}"
          f" smt_file {smt_file}"
          f" checks_before {checks_before_partition}"
          f" checks_between {checks_between_partitions}"
          f" strategy {strategy}"
          )
    my_partitions = get_partitions(partitioner, partitioner_options, number_of_partitions,
                                   output_file, smt_file,
                                   checks_before_partition, checks_between_partitions,
                                   strategy)
    print(f" {len(my_partitions)} partitions successfully made!")
else:
    my_partitions = None

# Now scatter partitions to the workers.
# For now, num partitions = num workers.
# In fact, list slicing does not seem to be support by the
#   mpi library. Note to self - might need to do a c++ impl
#   and interface with it here so that I can have a queue.
# my_partition = comm_world.scatter(my_partitions, root=0)


def run_a_partition(partition):
    tmpfilename = stitch_partition(partition, problem_path)
    result = run_solver(partitioner, tmpfilename)
    return result


with MPICommExecutor(MPI.COMM_WORLD, root=0) as executor:
    if executor is not None:
        answer = executor.map(run_a_partition, my_partitions)
        for a in answer:
            print("test", a)

# print("solver ran")
#
# if (my_rank != 0):
#     # maybe communicate the outputs from all workers to the main solver
#     print("coom.send")
#     comm_world.send(result, dest=0, tag=99)
# else:
#     print("collecting results")
#     rank = None
#     # Problem: this is blocking and waits for the longest partition.
#     # May be better to monitor the logs.
#     if result == "sat":
#         print("found result SAT")
#     else:
#         for rank in range(1, num_procs):
#             print(f"looking at rank {rank}")
#             result = comm_world.recv(source=rank, tag=99)
#             # Only one sat needs to exist for the whole problem to be sat.
#             if result == "sat":
#                 print("found result SAT")
#                 break
#         # TODO: return unknowns and errors properly.
#         print("found result UNSAT")
