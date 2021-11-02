

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from mpl_toolkits import mplot3d

df = pd.read_csv("../measurements.csv", index_col=0)
df.describe()

"""## 3D Scatter"""

mean_d = df.groupby(["Exams", "Percentage"]).mean().reset_index()
mean_d

(df.groupby(["Exams", "Percentage"]).count() > 1).any()

(df.groupby(["Exams", "Percentage"]).count() < 1).any()

#Plot 3D scatter

fig = plt.figure(figsize=(15,12))
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.invert_xaxis()

# Data for three-dimensional scattered points
for code, color, desc  in [(1, "Blues", "TopDown"), (2, "Oranges", "BottomUp")]:
  zdata = np.log(mean_d["Time_code{}".format(code)])
  xdata = mean_d["Exams"]
  ydata = mean_d["Percentage"]
  s = ax.scatter3D(xdata, ydata, zdata, depthshade=False, cmap=color);
  s.set_label('Code {} - {}'.format(code, desc))

ticks = np.arange(0, 20, 2) - 14
tick_labels = [r'$10^{%i}$'%(i) for i in ticks]

ax.set_zticks(ticks)
ax.set_zticklabels(tick_labels)
ax.set_xlabel('Number of Exams')
ax.set_ylabel('Probability of Exam Collision')
ax.set_zlabel('Time (s)')
ax.legend()

plt.show()
