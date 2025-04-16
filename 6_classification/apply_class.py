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

# Load the dataset
dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + 'csv_files/well_being.csv')

# To avoid convergence warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings("ignore")

# Target variable: 'category_goodday_1'
target = "category_goodday_2"

# Select input features
input_columns = ["What programme are you in?",
                "What is your gender?",
                "I have used ChatGPT to help me with some of my study assignments ",
                "When is your birthday (date)?",
                "WellBeing",
                "category_goodday_1",]

X = df[input_columns]
y = df[target]

# Encode categorical features
for col in X.select_dtypes(include=["object"]).columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

# Encode target variable
y = LabelEncoder().fit_transform(y.astype(str))

# Split the data: 2/3 training and 1/3 test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=13319817, stratify=y)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) # Fit on training data
X_test_scaled = scaler.transform(X_test)

# K-Nearest Neighbors

# Define parameter grid for grid search
knn_param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11, 13], # Number of neighbors to consider
    'weights': ['uniform', 'distance'], # Weight function used in prediction
    'metric': ['euclidean', 'manhattan']} # Distance metric to use

# Estimate the model
knn = KNeighborsClassifier()
knn_grid = GridSearchCV(knn, knn_param_grid, cv=10, scoring='accuracy', n_jobs=-1) # Using 10-fold cross-validation
knn_grid.fit(X_train_scaled, y_train) # Fit on training data

print("Best KNN Params.:", knn_grid.best_params_)

# Predict on test set using best estimator and compute Cohen's Kappa (performance metric)
y_pred_knn = knn_grid.best_estimator_.predict(X_test_scaled)
kappa_knn = cohen_kappa_score(y_test, y_pred_knn)
print("KNN Cohen's Kappa:", kappa_knn)
print("KNN Classification Report:\n", classification_report(y_test, y_pred_knn)) # Classification report contains other metrics mentioned in the lecture

# Neural Network (MLPClassifier)

# Define parameter grid for MLP
mlp_param_grid = {
    'hidden_layer_sizes': [(25,), (50,), (100,), (25,25), (50,50)], # Number of neurons in each hidden layer
    'alpha': [0.001, 0.01, 0.1], # Penalty for overfitting
    'activation': ['relu', 'tanh'], # Activation function used by neurons
    'solver': ['adam', 'sgd', 'lbfgs'], # Optimization algorithm
    'learning_rate': ['constant', 'adaptive']
}

# Estimate the model
mlp = MLPClassifier(max_iter=1000, random_state=13319817)
mlp_grid = GridSearchCV(mlp, mlp_param_grid, cv=10, scoring='accuracy', n_jobs=-1) # Using 10-fold cross-validation
mlp_grid.fit(X_train_scaled, y_train) # Fit on training data

print("Best MLP Params.:", mlp_grid.best_params_)

# Predict on test set using best estimator and compute Cohen's Kappa (performance metric)
y_pred_mlp = mlp_grid.best_estimator_.predict(X_test_scaled)
kappa_mlp = cohen_kappa_score(y_test, y_pred_mlp)
print("MLP Cohen's Kappa:", kappa_mlp)
print("MLP Classification Report:\n", classification_report(y_test, y_pred_mlp))