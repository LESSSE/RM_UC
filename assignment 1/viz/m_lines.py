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

# Plot Linear Regression

p_class = df.loc[:, ["Percentage"]].applymap(lambda x: str(x))
df['Time_code1'] = df["Time_code1"].apply(lambda y: math.log(y * (10 ** 6)))
p_index = p_class.applymap(lambda x: x in ["0.0", "0.25", "0.5", "0.75", "0.9", "1.0"])["Percentage"]
# p_index = p_class.applymap(lambda x: x in ["0.75"])["Percentage"]

grid = sns.lmplot(data=df.loc[p_index], x="Exams", y="Time_code1", hue="Percentage")
# grid = sns.regplot(data=df.loc[p_index], x="Exams", y="Time_code1")
# grid.set(yscale="log")
grid = grid.set_axis_labels("Exams", "log(Time_code1*10^6)")

plt.show()
