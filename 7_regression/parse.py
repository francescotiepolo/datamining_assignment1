#!/usr/bin/python3
import os
import json
import matplotlib.pyplot as plt
import pandas as pd

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
raw = []
with open(dir + "data/regression.json") as f:
    raw = json.load(f)

gamma_r2 = []
gamma_best = []
random_forest_r2 = []
random_forest_best = []
variance = []
columns = []
for row in raw:
    gamma_r2.append(row["gamma"]["r2"])
    gamma_best.append(row["gamma"]["Params"])
    random_forest_r2.append(row["random_forest"]["r2"])
    random_forest_best.append(row["random_forest"]["Params"])
    variance.append(sum(row["variance_ratio"]))
    columns.append(len(row["variance_ratio"]))

columns, gamma_r2, gamma_best, random_forest_r2, random_forest_best, variance = zip(*sorted(zip(columns, gamma_r2, gamma_best, random_forest_r2, random_forest_best, variance)))
plt.plot(columns, gamma_r2, label="Gamma")
plt.plot(columns, random_forest_r2, label="Random Forest")
plt.xlim(0, 60)
plt.legend()
plt.savefig(dir + "figs/r2.pdf")
plt.clf()

best_parameters = list(map(lambda x: {"Gamma Alpha": x[0]["alpha"], "Gamma Solver": x[0]["solver"], "Forest Max Attributes": x[1]["max_features"], "Forest Number of Estimators": x[1]["n_estimators"]}, zip(gamma_best, random_forest_best)))
variance_data = list(map(lambda x: {"Variance": x}, variance))
pd.DataFrame(best_parameters, index=columns).to_latex(dir + "figs/parameters_data.tex")
pd.DataFrame(variance_data, index=columns).to_latex(dir + "figs/variance.tex")