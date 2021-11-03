mean_d = df.groupby(["Exams", "Percentage"]).mean().reset_index()
