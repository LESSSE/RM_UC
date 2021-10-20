import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time

seed_1 = 1325
seed_2 = 31235
data_file = "data.in"
avg_test = 5


def run_test(sizes, percentages, cutoff_time):
    file1 = "code1_results.txt"
    file2 = "code2_results.txt"

    os.system(f'rm -f code1_results.txt code2_results.txt')

    code1_times = []
    code2_times = []

    for p in percentages:
        for s in sizes:
            code1_time = []
            code2_time = []
            for i in range(avg_test):
                os.system(f'python3 gen.py {s} {p} {seed_1} {data_file}')
                os.system(f'echo "______\\nExams: {s} | Percentage: {p}" | tee -a {file1} {file2}')
                os.system(f'./code1 {seed_2} {cutoff_time} {data_file} >> {file1}')
                os.system(f'./code2 {seed_2} {cutoff_time} {data_file} >> {file2}')

                code1_result = open(file1).readlines()[-1][:-1]
                code2_result = open(file2).readlines()[-1][:-1]
                print("CODE1:", code1_result, "Iter: ", i+1)  # print last line from code1 results
                print("CODE2:", code2_result, "Iter: ", i+1)  # print last line from code2 results

                code1_time.append(float(code1_result.split(' ')[1]))
                code2_time.append(float(code2_result.split(' ')[1]))

                if code1_result.split(' ')[0] == '-1' and code2_result.split(' ')[0] == '-1':
                    break

                if open(file1).readlines()[-1].startswith("Exams") or open(file2).readlines()[-1].startswith("Exams"):
                    # if some of the processes didn't return something then it stops cause it means a sigint was signaled
                    # and stopped the subprocess
                    sys.exit(0)
            code1_times.append(np.average(code1_time))
            code2_times.append(np.average(code2_time))

    return code1_times, code2_times


if __name__ == '__main__':
    start_time = time.time()
    sizes = np.arange(20, 51, 1)
    # sizes = [20]
    # percentages = np.linspace(0, 1, 21)
    percentages = [0.4]
    cutoff_time = 100  # seconds

    code_times1, code_times2 = run_test(sizes, percentages, cutoff_time)

    x = sizes if len(sizes) > len(percentages) else percentages
    plt.scatter(x, code_times1, label="code1")
    plt.scatter(x, code_times2, label="code2")
    plt.show()

    print("Total program running time: ", time.time()-start_time, " seconds")

