from parse import parse
import pandas as pd

code = "code1"

cols = ["Exams", "Percentage", "Solution_"+code, "Time_"+code]
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
                l1 = parse("Exams: {} | Percentage: {}", lines[l+1])
                l2 = parse("{} {}", lines[l + 2])
                df2 = pd.DataFrame([[int(l1[0]), float(l1[1]), int(l2[0]), float(l2[1])]], columns=cols)
                df = df.append(df2, ignore_index = True)
            except:
                pass

print(df)
df.to_csv(export_csv_path)

