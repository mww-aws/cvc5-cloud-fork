import subprocess
import os
import json
from pathlib import Path


def get_input_json(request_directory):
  input = os.path.join(request_directory, "input.json")
  with open(input) as f:
    return json.loads(f.read())


"""
Make partitions by executing the partitioner with the provided options. 

  partitioner : the executable to use for partitioning
  partitioner_options : extra cli arguments to pass to partitioner
  number_of_partitions : The desired number of partitions to be made. 
  output_file : The file that partitions are written to. 
  smt_file : The full path of the smt2 benchmark file being partitioned.
  checks_before_partition : number of checks before partitioner starts 
                            making partitions
  checks_between_partitions : number of checks between subsequent partitions
  strategy : the partitioning strategy to send to the partitioner
  debug : flag that indicates whether debug information should be printed
  returns : void

TODO: Probably want to check for errors and/or confirm that the 
partitions were actually made and return something like a bool.
"""


def make_partitions(partitioner, partitioner_options, number_of_partitions,
                    output_file, smt_file,
                    checks_before_partition, checks_between_partitions,
                    strategy, debug=False):
  # Build the partition command
  partition_command = (
      f"{partitioner} --compute-partitions={number_of_partitions} "
      f"--lang=smt2 --partition-strategy={strategy} "
      f"--checks-before-partition={checks_before_partition} "
      f"--checks-between-partitions={checks_between_partitions} "
      f"{partitioner_options} {smt_file}"
  )

  output = subprocess.check_output(
      partition_command, shell=True)
  partitions = output.decode("utf-8").strip().split('\n')
  return partitions[0: len(partitions) - 1]


"""
Make a copy of the partitioned problem and append a cube to it for each cube
that is in the list of partitions.
  partitions : The list of cubes to be appended to copies of the partitioned
               problem. 
  stitched_directory : The directory in which the stitched files will be 
                       written.  
  parent_file : The file that was partitioned. 
  debug : flag that indicates whether debug information should be printed
  returns : void
"""


def stitch_partition(partition, j, stitched_directory, parent_file, debug=False):

  new_bench_filename = (
      f"{stitched_directory}{Path(parent_file).stem}_p{j}.smt2")
  # TODO: Create the dir in the main file?

  # Read the original contents in
  # TODO: MAKE THIS FASTER - should be able to read one and write
  #     the other at the same time
  with open(parent_file) as bench_file:
    bench_contents = bench_file.readlines()

  # Append the cube to the contents and write to the new file.
  with open(new_bench_filename, 'w+') as new_bench_file:
    bench_contents[bench_contents.index("(check-sat)\n"):
                   bench_contents.index("(check-sat)\n")] = \
        "( assert " + partition + " ) \n"
    new_bench_file.write("".join(bench_contents))
  return new_bench_filename


def run_solver(solver_executable, stitched_file):
  # Build the partition command
  solve_command = (
      f"{solver_executable} --lang=smt2 {stitched_file}"
  )

  output = subprocess.check_output(
      solve_command, shell=True).decode("utf-8").strip()
  if "unsat" in output:
    return "unsat"
  elif "sat" in output:
    return "sat"
  elif "unknown" in output:
    return "unknown"
  else:
    return "error"
