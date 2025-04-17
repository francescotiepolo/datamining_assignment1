#!/usr/bin/python3
import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import PoissonRegressor
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score

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
    "Parsed Give a random number",
    "Parsed What is your stress level (0-100)?"
]
ignore.extend(base_features)
x = x.drop(ignore, axis=1)
x = x.join(encoded)

y = df["Parsed What is your stress level (0-100)?"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=13319817)

pca = PCA().fit(x_train)
x_train = pca.transform(x_train)
x_test = pca.transform(x_test)

def poisson_prediction(x_train, y_train, x_test, y_test):
    param_grid = {
        "alpha": [0.125, 0.25, 0.5, 1, 2, 4, 8],
        "solver": ["lbfgs", "newton-cholesky"]
    }
    poisson = PoissonRegressor()
    poisson_grid = GridSearchCV(poisson, param_grid, cv=10, scoring="r2", n_jobs=-1)
    poisson_grid.fit(x_train, y_train)
    print("Best Poisson Params.:", poisson_grid.best_params_)

    y_pred = poisson_grid.best_estimator_.predict(x_test)
    print(r2_score(y_test, y_pred))


def random_forest_prediction(x_train, y_train, x_test, y_test):
    param_grid = {
        "n_estimators": [40, 60, 80, 100, 120, 140, 160],
        "max_features": list(map(lambda x: x+1, range(0, len(x_train.columns))))
    }
    forest = RandomForestRegressor(
        random_state=13319817
    )
    forest_grid = GridSearchCV(forest, param_grid, cv=10, scoring="r2", n_jobs=-1)
    forest_grid.fit(x_train, y_train)
    print("Best Random Forest Params.:", forest_grid.best_params_)

    y_pred = forest_grid.best_estimator_.predict(x_test)
    print(r2_score(y_test, y_pred))

poisson_prediction(x_train, y_train, x_test, y_test)
random_forest_prediction(x_train, y_train, x_test, y_test)