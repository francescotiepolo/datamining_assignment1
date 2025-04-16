from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

def decision_tree(df, output, input): # Output for missing values based on Decision Tree Classifier
    df_copy = df.copy()
    # Devide the data into known and unknown values
    known = df_copy[output].notnull()
    unknown = ~known

    X = df_copy[input].astype(str)
    X_known = X[known]
    X_unknown = X[unknown]
    Y_known = df_copy.loc[known, output]

    # Prepare the data for the Decision Tree Classifier
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_known_encoded = encoder.fit_transform(X_known)

    if X_unknown.shape[0] > 0:
        X_unknown_encoded = encoder.transform(X_unknown) # Transform the unknown values according to the previously found fit
        tree = DecisionTreeClassifier(max_depth=5, random_state=0) # Max 5 levels
        tree.fit(X_known_encoded, Y_known) # Fit the model on the known values
        Y_pred = tree.predict(X_unknown_encoded) # Predict the unknown values
        df_copy.loc[unknown, output] = Y_pred
    
    return df_copy

def random_forest(df, output, input): # Output for missing values based on Random Forest Regressor
    df_copy = df.copy()
    # Devide the data into known and unknown values
    known = df_copy[output].notnull()
    unknown = ~known

    X = df_copy[input].astype(str)
    X_known = X[known]
    X_unknown = X[unknown]
    Y_known = df_copy.loc[known, output]

    # Prepare the data for the Random Forest Regressor
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_known_encoded = encoder.fit_transform(X_known)

    if X_unknown.shape[0] > 0:
        X_unknown_encoded = encoder.transform(X_unknown) # Transform the unknown values according to the previously found fit
        forest = RandomForestRegressor(n_estimators=100, max_depth=None, random_state=0) # 100 trees with no max levels
        forest.fit(X_known_encoded, Y_known) # Fit the model on the known values
        Y_pred = forest.predict(X_unknown_encoded) # Predict the unknown values
        df_copy.loc[unknown, output] = Y_pred
        
    return df_copy