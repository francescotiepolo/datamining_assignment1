from sklearn.tree import DecisionTreeClassifier
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
    X_unknown_encoded = encoder.transform(X_unknown)

    tree = DecisionTreeClassifier(max_depth=5, random_state=0)
    tree.fit(X_known_encoded, Y_known)
    Y_pred = tree.predict(X_unknown_encoded)

    df_copy.loc[unknown, output] = Y_pred
    return df_copy