import os
import sys
import numpy as np
from parse import parse
import pandas as pd
import math
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('-1', '--seed1', type=int, default=1325, help='initial seed for the graph generation')
parser.add_argument('-2', '--seed2', type=int, default=31235, help='initial seed for node verification')
parser.add_argument('-s', '--seed', type=int, default=63, help='global seed')
parser.add_argument('-n', '--nsamples', type=int, default=36, help='number of samples for each pair of parameters')
parser.add_argument('-e', '--examrange', type=str, default="(5, 25, 1)", help='(min, max, step) for ranging the param exams')
parser.add_argument('-p', '--probrange', type=str, default="(0, 1, 0.01)", help='(min, max, step) for ranginf the param prob')

args = parser.parse_args()


seed = args.seed
random.seed(seed)

seed_1 = args.seed1
seed_2 = args.seed2
n_samples = args.nsamples

args.probrange = eval(args.probrange)
args.examrange = eval(args.examrange)

if type(args.probrange) is not tuple or len(args.probrange) != 3:
    exit(-1)

if type(args.examrange) is not tuple or len(args.examrange) != 3:
    exit(-1)

prob_lin_args = (args.probrange[0],
                 args.probrange[1],
                 math.ceil((args.probrange[1]-args.probrange[0])/args.probrange[2])+1)

exams = np.arange(*args.examrange)
probs = np.linspace(*prob_lin_args)

cutoff_time = 300 #seconds

data_file = "data.in"

file1 = "code1_results.txt"
file_seeds1 = "code1_seeds.txt"

file2 = "code2_results.txt"
file_seeds2 = "code2_seeds.txt"

os.system("rm -f {} {}".format(file1, file2))

for s in exams:
    for p in probs:
        for i_seed_1 in range(math.ceil(math.sqrt(n_samples))):
            if seed:
                rand_gen = random.randint(1, 100)
            else:
                rand_gen = 0
            for i_seed_2 in range(math.ceil(math.sqrt(n_samples))):
                if seed:
                    rand_code1 = random.randint(1, 100)
                    rand_code2 = random.randint(1, 100)
                else:
                    rand_code1 = 0
                    rand_code2 = 0
                os.system(f'python3 gen.py {s} {p} {seed_1+i_seed_1+rand_gen} {data_file}')
                os.system(f'echo "______\\nExams: {s} | Percentage: {p}" | tee -a {file1} {file2}')

                os.system(f'echo "Seed1: {seed_1+i_seed_1+rand_gen} | Seed2: {seed_2+i_seed_2+rand_code1}" >> {file1}')
                os.system(f'./code1 {seed_2+i_seed_2+rand_code1} {cutoff_time} {data_file} >> {file1}')

                os.system(f'echo "Seed1: {seed_1+i_seed_1+rand_gen} | Seed2: {seed_2+i_seed_2+rand_code2}" >> {file2}')
                os.system(f'./code2 {seed_2+i_seed_2+rand_code2} {cutoff_time} {data_file} >> {file2}')

                print("CODE1:", open(file1).readlines()[-1][:-1]) # print last line from code1 results
                print("CODE2:", open(file2).readlines()[-1][:-1]) # print last line from code2 results
                if open(file1).readlines()[-1].startswith("Exams") or open(file2).readlines()[-1].startswith("Exams"):
                    # if some of the processes didn't return something then it stops cause it means a sigint was signaled
                    # and stopped the subprocess
                    sys.exit(0)

for i in [1, 2]:
    code = "code{}".format(i)

    cols = ["Exams", "Percentage", "Seed1", "Seed2", "Solution_"+code, "Time_"+code,]
    csv = "measurements.csv"
    export_csv_path = "measurements.csv"

    if csv is None:
        df = pd.DataFrame(columns=cols)
    else:
        df = pd.read_csv(csv, index_col=0)

    with open("{}_results.txt".format(code)) as file:
        lines = file.readlines()
        for l in range(len(lines)):
            if lines[l] == "______\n":
                try:
                    l1 = parse("Exams: {} | Percentage: {}", lines[l + 1])
                    l2 = parse("Seed1: {} | Seed2: {}", lines[l + 2])
                    l3 = parse("{} {}", lines[l + 3])
                    df2 = pd.DataFrame([[int(l1[0]), float(l1[1]), int(l2[0]), int(l2[1]), int(l3[0]), float(l3[1])]], columns=cols)
                    df = df.append(df2, ignore_index=True)
                except:
                    pass

    print(df)
    df.to_csv(export_csv_path)
