from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

def decision_tree(df, output, input):
    df_copy = df.copy()
    known = df_copy[output].notnull()
    unknown = ~known

    X = df_copy[input].fillna("unknown").astype(str)
    X_known = X[known]
    X_unknown = X[unknown]
    Y_known = df_copy.loc[known, output]

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_known_encoded = encoder.fit_transform(X_known)

    if X_unknown.shape[0] > 0:
        X_unknown_encoded = encoder.transform(X_unknown)
        from sklearn.tree import DecisionTreeClassifier
        tree = DecisionTreeClassifier(max_depth=5, random_state=0)
        tree.fit(X_known_encoded, Y_known)
        Y_pred = tree.predict(X_unknown_encoded)
        df_copy.loc[unknown, output] = Y_pred
    
    return df_copy

def random_forest(df, output, input):
    df_copy = df.copy()
    known = df_copy[output].notnull()
    unknown = ~known

    X = df_copy[input].fillna("unknown").astype(str)
    X_known = X[known]
    X_unknown = X[unknown]
    Y_known = df_copy.loc[known, output]

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_known_encoded = encoder.fit_transform(X_known)

    if X_unknown.shape[0] > 0:
        X_unknown_encoded = encoder.transform(X_unknown)
        forest = RandomForestRegressor(
            n_estimators=100,
            max_depth=None,
            random_state=0
        )
        forest.fit(X_known_encoded, Y_known)
        Y_pred = forest.predict(X_unknown_encoded)
        df_copy.loc[unknown, output] = Y_pred
        
    return df_copy