#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import os
dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
parent = dir + ".." + os.path.sep
df = pd.read_csv(parent + "ODI-2025-parsed.csv",sep=";")

def histogram(df: pd.DataFrame, column: str, lower_bound: float, upper_bound: float, cut_off: float | None, suffix: str):
    data = []
    invalid_count = 0
    outside = []
    for i, row in df.iterrows():
        try:
            value = float(row[column].replace(",", "."))
            if cut_off is not None and value > cut_off:
                invalid_count += 1
                outside.append(value)
            else:
                data.append(value)
        except:
            invalid_count += 1

    plt.clf()
    plt.hist(data)
    plt.savefig(f"{dir}most_{suffix}.pdf")
    filtered = list(filter(lambda x: x >= lower_bound and x <= upper_bound, data))
    plt.clf()
    plt.hist(filtered)
    plt.savefig(f"{dir}filtered_{suffix}.pdf")
    print(invalid_count)
    print(outside)
    print(len(outside))
    print(len(data) - len(filtered))

def stress(df: pd.DataFrame):
    histogram(df, "What is your stress level (0-100)?", 0, 100, 80000, "stress")

def students(df: pd.DataFrame):
    histogram(df, "How many students do you estimate there are in the room?", 0, 600, 60000, "students")

def sports(df: pd.DataFrame):
    histogram(df, "How many hours per week do you do sports (in whole hours)? ", 0, 50, 900, "sports")

stress(df)
students(df)
sports(df)