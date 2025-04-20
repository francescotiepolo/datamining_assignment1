#!/usr/bin/python3
import pandas as pd
import os
from naive_bayes_func_trial import naive_bayes_imputer

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + 'csv_files/joined.csv')

# List the columns we want to use to feed the models
input_columns = ["Have you taken a course on machine learning?",
                 "Have you taken a course on information retrieval?",
                 "Have you taken a course on statistics?",
                 "Have you taken a course on databases?",
                 "What is your gender?",
                 "I have used ChatGPT to help me with some of my study assignments "]

# Apply Naive Bayes to categorical variables
df = naive_bayes_imputer(df, "category_goodday_1", input_columns)
input_columns.append("category_goodday_1")
df = naive_bayes_imputer(df, "category_goodday_2", input_columns)
input_columns.append("category_goodday_2")
df = naive_bayes_imputer(df, "What programme are you in?", input_columns)
input_columns.append("What programme are you in?")
df = naive_bayes_imputer(df, "When is your birthday (date)?", input_columns)
input_columns.append("When is your birthday (date)?")

df.to_csv(dir + 'csv_files/filled_naive_bayes_trial.csv', index=False)