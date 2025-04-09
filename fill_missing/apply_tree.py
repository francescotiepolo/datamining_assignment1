import pandas as pd
import os
from tree_func import decision_tree

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + 'csv_files/joined.csv')

input_columns = ["Have you taken a course on machine learning?",
                 "Have you taken a course on information retrieval?",
                 "Have you taken a course on statistics?",
                 "Have you taken a course on databases?",
                 "What is your gender?",
                 "I have used ChatGPT to help me with some of my study assignments "]

df = decision_tree(df, "category_goodday_1", input_columns)
df = decision_tree(df, "category_goodday_2", input_columns)

df.to_csv(dir + 'csv_files/filled.csv', index=False)