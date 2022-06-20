from mpi4py import MPI
import subprocess
import pdb 

partitioner = "/Users/amaleewilson/cvc5/build/bin/cvc5"
strategy = "strict-cube"
number_of_partitions = "4"
output_file = "/Users/amaleewilson/aws-satcomp-solver-sample/local-mpi/partition_output"
checks_before_partition = "500"
checks_between_partitions = "500"
partitioner_options = "--append-learned-literals-to-cubes"
p0 = "--produce-learned-literals"
smt_file = ("/Users/amaleewilson/Downloads/_array_monotonic.i_3_2_2.bpl_11.smt2")

# This version writes the partitions to a file. 
# partition_command = [partitioner, 
#     f"--compute-partitions={number_of_partitions}",
#     f"--partition-strategy={strategy}",
#     f"--checks-before-partition={checks_before_partition}",
#     f"--write-partitions-to={output_file}",
#     f"--checks-between-partitions={checks_between_partitions}",
#     partitioner_options, p0,
#     smt_file]
# 
# proc = subprocess.run(partition_command, check=True)

# This version gets the output from the partition command. 
partition_command = [partitioner, 
    f"--compute-partitions={number_of_partitions}",
    f"--partition-strategy={strategy}",
    f"--checks-before-partition={checks_before_partition}",
    f"--checks-between-partitions={checks_between_partitions}",
    partitioner_options, p0,
    smt_file]

output = subprocess.check_output(partition_command).decode("utf-8").strip()
print(output[0])