# Import necessary libraries
import pandas as pd
import os
import warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import cohen_kappa_score, classification_report

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + 'csv_files/well_being.csv')

os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings("ignore")

# Target variable: 'category_goodday_1'
target = "category_goodday_2"

input_columns = ["What programme are you in?",
                "What is your gender?",
                "I have used ChatGPT to help me with some of my study assignments ",
                "When is your birthday (date)?",
                "WellBeing",
                "category_goodday_1",]
X = df[input_columns]
y = df[target]

for col in X.select_dtypes(include=["object"]).columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

y = LabelEncoder().fit_transform(y.astype(str))

# Split the data: 2/3 training and 1/3 test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=42, stratify=y)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# K-Nearest Neighbors

# Define parameter grid for grid search
knn_param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11, 13],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

knn = KNeighborsClassifier()
knn_grid = GridSearchCV(knn, knn_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", ConvergenceWarning)
    knn_grid.fit(X_train_scaled, y_train)

print("Best KNN Params.:", knn_grid.best_params_)

# Predict on test set using best estimator
y_pred_knn = knn_grid.best_estimator_.predict(X_test_scaled)
kappa_knn = cohen_kappa_score(y_test, y_pred_knn)
print("KNN Cohen's Kappa:", kappa_knn)
print("KNN Classification Report:\n", classification_report(y_test, y_pred_knn))

# Neural Network (MLPClassifier)

# Define parameter grid for MLP
mlp_param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (50,50)],
    'alpha': [0.00001, 0.0001, 0.001, 0.01],
    'activation': ['relu', 'tanh'],
    'solver': ['adam', 'sgd'],
    'learning_rate': ['constant', 'adaptive']
}

mlp = MLPClassifier(max_iter=500, random_state=42)
mlp_grid = GridSearchCV(mlp, mlp_param_grid, cv=5, scoring='accuracy', n_jobs=-1)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", ConvergenceWarning)
    mlp_grid.fit(X_train_scaled, y_train)

print("Best MLP Params.:", mlp_grid.best_params_)

# Predict on test set using best estimator
y_pred_mlp = mlp_grid.best_estimator_.predict(X_test_scaled)
kappa_mlp = cohen_kappa_score(y_test, y_pred_mlp)
print("MLP Cohen's Kappa:", kappa_mlp)
print("MLP Classification Report:\n", classification_report(y_test, y_pred_mlp))