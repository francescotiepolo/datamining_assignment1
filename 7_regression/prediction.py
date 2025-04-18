#!/usr/bin/python3
import os
import pandas as pd
import warnings
import json
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import GammaRegressor
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings("ignore")

def gamma_prediction(x_train, y_train, x_test, y_test):
    print("gamma")
    param_grid = {
        "alpha": [0.125, 0.25, 0.5, 1, 2, 4, 8],
        "solver": ["lbfgs", "newton-cholesky"]
    }
    gamma = GammaRegressor()
    gamma_grid = GridSearchCV(gamma, param_grid, cv=10, scoring="r2", n_jobs=-1)
    gamma_grid.fit(x_train, y_train)

    y_pred = gamma_grid.best_estimator_.predict(x_test)
    return {"Params": gamma_grid.best_params_, "r2": float(r2_score(y_test, y_pred))}


def random_forest_prediction(x_train, y_train, x_test, y_test):
    print("Random Forest")
    param_grid = {
        "n_estimators": [40, 60, 80, 100, 120, 140, 160],
        "max_features": list(map(lambda x: x+1, range(0, len(x_train[0]))))
    }
    forest = RandomForestRegressor(
        random_state=13319817
    )
    forest_grid = GridSearchCV(forest, param_grid, cv=10, scoring="r2", n_jobs=-1)
    forest_grid.fit(x_train, y_train)

    y_pred = forest_grid.best_estimator_.predict(x_test)
    return {"Params": forest_grid.best_params_, "r2": float(r2_score(y_test, y_pred))}

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + "csv_files/well_being.csv")

encoder = OneHotEncoder(handle_unknown="ignore")
base_features = [
    "What programme are you in?",
    "Have you taken a course on machine learning?",
    "Have you taken a course on information retrieval?",
    "Have you taken a course on statistics?",
    "Have you taken a course on databases?",
    "What is your gender?",
    "I have used ChatGPT to help me with some of my study assignments ",
    "When is your birthday (date)?",
    "category_goodday_1",
    "category_goodday_2"
]
encoded = encoder.fit_transform(pd.DataFrame(df[base_features]))
encoded = pd.DataFrame(encoded.toarray(), columns=encoder.get_feature_names_out())

x = df.copy(deep=True)
ignore = [
    "Timestamp",
    "How many students do you estimate there are in the room?",
    "What is your stress level (0-100)?",
    "How many hours per week do you do sports (in whole hours)? ",
    "Give a random number",
    "Time you went to bed Yesterday",
    "What makes a good day for you (1)?",
    "What makes a good day for you (2)?",
    "SleepDeviation",
    "Norm.SleepDeviation",
    "Norm.Stress",
    "Norm.Sport",
    "WellBeing",
    "Parsed How many students do you estimate there are in the room?",
    "Parsed What is your stress level (0-100)?",
    "Parsed How many hours per week do you do sports (in whole hours)?",
    "Parsed Give a random number",
    "Parsed Time you went to bed Yesterday"
]
ignore.extend(base_features)
x = x.drop(ignore, axis=1)
x = x.join(encoded)

y = df["WellBeing"]

data = []
columns = list(range(5,len(x.columns),5))
columns.append(len(x.columns))
for i in columns:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=13319817)

    pca = PCA(svd_solver="full", n_components=i).fit(x_train)
    x_train = pca.transform(x_train)
    x_test = pca.transform(x_test)
    print(len(x_train[0]))

    gamma_data = gamma_prediction(x_train, y_train, x_test, y_test)
    random_forest_data = random_forest_prediction(x_train, y_train, x_test, y_test)
    data.append({
        "gamma": gamma_data,
        "random_forest": random_forest_data,
        "variance_ratio": pca.explained_variance_ratio_.tolist()
    })

with open("./data/regression.json", mode="w") as f:
    json.dump(data, f)