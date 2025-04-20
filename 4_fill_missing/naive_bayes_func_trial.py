from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder

def naive_bayes_imputer(df, target_column, input_columns):
    """
    Fill missing values in a categorical column using Naive Bayes classification
    """
    df_transforming = df.copy()
    
    # Split data into rows with and without missing values
    filled_data = df_transforming[df_transforming[target_column].notna()]
    unfilled_data = df_transforming[df_transforming[target_column].isna()]
    
    if unfilled_data.empty or filled_data.empty:
        return df
    
    X = filled_data[input_columns]
    y = filled_data[target_column]
    
    # Encode categorical variables if needed
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    model = CategoricalNB()
    
    # Convert input features to categorical codes
    X_encoded = X.apply(lambda x: x.astype('category').cat.codes)
    
    model.fit(X_encoded, y_encoded)
    
    X_missing = unfilled_data[input_columns]
    X_missing_encoded = X_missing.apply(lambda x: x.astype('category').cat.codes)
    predicted_encoded = model.predict(X_missing_encoded)
    predicted = le.inverse_transform(predicted_encoded)
    
    # Fill missing values
    df.loc[df[target_column].isna(), target_column] = predicted
    
    return df
