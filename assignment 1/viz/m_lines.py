# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

from mpl_toolkits import mplot3d

df = pd.read_csv("../measurements.csv", index_col=0)
df.describe()

"""## Linear Regression"""

mean_d = df.groupby(["Exams", "Percentage"]).mean().reset_index()
mean_d

(df.groupby(["Exams", "Percentage"]).count() > 1).any()

(df.groupby(["Exams", "Percentage"]).count() < 1).any()

df_groups = df.groupby(["Percentage", "Exams"]).mean().reset_index()
# prob_1 = df_groups[(df_groups.Percentage == 1)]

# p_class = df.loc[:, ["Exams"]].applymap(lambda x: str(x))
# p_index = p_class.applymap(lambda x: x in ["6", "9", "12", "15", "18"])["Exams"]

#df['Time_code1'] = df["Time_code1"].apply(lambda y: math.log(y * (10 ** 6)))
# grid = sns.lmplot(data=df.loc[p_index], x="Percentage", y="Time_code1", hue="Exams")
# grid = grid.set_axis_labels("Percentage", "log(log(Time_code1*10^6))")
#
# plt.show()
#
# df['Time_code1'] = df["Time_code1"].apply(lambda y: math.log(y * (10 ** 6)))
# grid = sns.lmplot(data=df.loc[p_index], x="Percentage", y="Time_code1", hue="Exams")
# grid = grid.set_axis_labels("Percentage", "log(log(Time_code1*10^6))")
#
# plt.show()

# Plot Linear Regression
p_class = df.loc[:, ["Exams"]].applymap(lambda x: str(x))
time_code = "Time_code2"
# df[time_code] = df[time_code].apply(lambda y: math.log(y * (10 ** 6)))
# df[time_code] = df[time_code].apply(lambda y: math.log(y * (10 ** 6)))
for e in range(6, 16, 1):

    p_index = p_class.applymap(lambda x: x in [str(e)])["Exams"]

    grid = sns.regplot(data=df.loc[p_index], x="Percentage", y=time_code, line_kws={"color": "red"})
    grid.set(ylabel=f"log({time_code}*10^6)", title=f"Exams = {str(e)}")

    plt.show()
