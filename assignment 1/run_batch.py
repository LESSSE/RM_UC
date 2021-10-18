import os
import sys
import numpy as np

seed_1 = 1325
seed_2 = 31235
data_file = "data.in"

sizes = np.arange(5, 15)
percentages = np.linspace(0, 1, 101)
cutoff_time = 300 #seconds

file1 = "code1_results.txt"
file2 = "code2_results.txt"

os.system(f'rm -f code1_results.txt code2_results.txt')

for s in sizes:
    for p in percentages:
        os.system(f'python3 gen.py {s} {p} {seed_1} {data_file}')
        os.system(f'echo "______\\nExams: {s} | Percentage: {p}" | tee -a {file1} {file2}')
        os.system(f'./code1 {seed_2} {cutoff_time} {data_file} >> {file1}')
        os.system(f'./code2 {seed_2} {cutoff_time} {data_file} >> {file2}')
        print("CODE1:", open(file1).readlines()[-1][:-1]) # print last line from code1 results
        print("CODE2:", open(file2).readlines()[-1][:-1]) # print last line from code2 results
        if open(file1).readlines()[-1].startswith("Exams") or open(file2).readlines()[-1].startswith("Exams"):
            # if some of the processes didn't return something then it stops cause it means a sigint was signaled
            # and stopped the subprocess
            sys.exit(0)
