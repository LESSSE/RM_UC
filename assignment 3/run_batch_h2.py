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
parser.add_argument('-n', '--nsamples', type=int, default=1000, help='number of samples for each pair of parameters')

args = parser.parse_args()


seed = args.seed
random.seed(seed)

seed_gen = args.seed1
seed_run = args.seed2
n_samples = args.nsamples

probs = np.array([0])

cutoff_time = 300 #seconds

data_file = "data.in"

file1 = "code1_results.txt"
file_seeds1 = "code1_seeds.txt"

file2 = "code2_results.txt"
file_seeds2 = "code2_seeds.txt"

os.system("rm -f {} {}".format(file1, file2))

for p in probs:
    for i in range(n_samples):
        s = np.random.randint(1, 50)

        rand_gen = random.randint(1, 100)

        os.system(f'python3 gen.py {s} {p} {seed_gen + rand_gen} {data_file}')

        for c in ["Code1", "Code2"]:

            if c == "Code1":
                file_ = file1
            else:
                file_ = file2
                print(file_)

            rand_run = random.randint(1, 100)

            os.system(f'echo "______\nExams: {s} | Percentage: {p}" >> {file_} ')

            os.system(f'python3 gen.py {s} {p} {seed_gen+rand_gen} {data_file}')
            os.system(f'echo "______\nExams: {s} | Percentage: {p}" >> {file_} ')

            os.system(f'echo "Seed1: {seed_gen+rand_gen} | Seed2: {seed_run+rand_run}" >> {file_}')
            os.system(f'./{c.lower()} {seed_run+rand_run} {cutoff_time} {data_file} >> {file_}')

            print(f'{c.upper()}:', open(file1).readlines()[-1][:-1]) # print last line from code1 results


csv = None
for i in [1, 2]:
    code = "code{}".format(i)

    cols = ["Exams", "Percentage", "Seed1", "Seed2", "Solution_"+code, "Time_"+code,]
    export_csv_path = "measurements_h2.csv"

    if csv is None:
        csv = "measurements_h2.csv"
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

