#!/usr/bin/python3
import pandas as pd
import os
from tree_func import decision_tree, random_forest

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
<<<<<<< HEAD
df = decision_tree(df, "What programme are you in?", input_columns)
df = decision_tree(df, "When is your birthday (date)?", input_columns)
=======
df = random_forest(df, "Parsed Time you went to bed Yesterday", input_columns)
df = random_forest(df, "Parsed Give a random number", input_columns)
df = random_forest(df, "Parsed How many hours per week do you do sports (in whole hours)?", input_columns)
df = random_forest(df, "Parsed What is your stress level (0-100)?", input_columns)
df = random_forest(df, "Parsed How many students do you estimate there are in the room?", input_columns)

>>>>>>> origin/exploration
df.to_csv(dir + 'csv_files/filled.csv', index=False)