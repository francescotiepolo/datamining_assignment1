from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder

def naive_bayes_imputer(df, target_column, input_columns):
    """
    Fill missing values in a categorical column using Naive Bayes classification
    """
    # Create a copy to avoid SettingWithCopyWarning
    df_working = df.copy()
    
    # Split data into rows with and without missing values
    known_data = df_working[df_working[target_column].notna()]
    unknown_data = df_working[df_working[target_column].isna()]
    
    # If no missing values or no known data, return original
    if unknown_data.empty or known_data.empty:
        return df
    
    # Prepare features and target
    X = known_data[input_columns]
    y = known_data[target_column]
    
    # Encode categorical variables if needed
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Initialize and train Naive Bayes classifier
    model = CategoricalNB()
    
    # Convert input features to categorical codes
    X_encoded = X.apply(lambda x: x.astype('category').cat.codes)
    
    model.fit(X_encoded, y_encoded)
    
    # Predict missing values
    X_missing = unknown_data[input_columns]
    X_missing_encoded = X_missing.apply(lambda x: x.astype('category').cat.codes)
    predicted_encoded = model.predict(X_missing_encoded)
    predicted = le.inverse_transform(predicted_encoded)
    
    # Fill the missing values
    df.loc[df[target_column].isna(), target_column] = predicted
    
    return df
