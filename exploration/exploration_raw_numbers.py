#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import os
dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
parent = dir + ".." + os.path.sep
df = pd.read_csv(parent + "csv_files" + os.path.sep + "ODI-2025.csv",sep=";")

def histogram(df: pd.DataFrame, column: str, lower_bound: float, upper_bound: float, cut_off: float | None, suffix: str):
    data = []
    invalid_count = 0
    outside = []
    for i, row in df.iterrows():
        try:
            value = float(row[column].replace(",", "."))
            if cut_off is not None and value > cut_off:
                outside.append(value)
            else:
                data.append(value)
        except:
            invalid_count += 1

    plt.clf()
    plt.title(f"Most {column}")
    plt.hist(data)
    plt.savefig(f"{dir}most_{suffix}.pdf")
    filtered = list(filter(lambda x: x >= lower_bound and x <= upper_bound, data))
    plt.clf()
    if suffix == "students":
        plt.hist(filtered, bins=list(range(0, 650, 50)))
    else:
        plt.hist(filtered)
    plt.title(f"Strict {column}")
    plt.savefig(f"{dir}filtered_{suffix}.pdf")
    print(suffix)
    print("Number of invalid", invalid_count)
    print("Outside general valid range", outside)
    print("Number of instances outside of general valid range", len(outside))
    print("Number of instances outside of strict valid range", len(data) - len(filtered))

def stress(df: pd.DataFrame):
    histogram(df, "What is your stress level (0-100)?", 0, 100, 80000, "stress")

def students(df: pd.DataFrame):
    histogram(df, "How many students do you estimate there are in the room?", 0, 600, 60000, "students")

def sports(df: pd.DataFrame):
    histogram(df, "How many hours per week do you do sports (in whole hours)? ", 0, 50, 900, "sports")

stress(df)
students(df)
sports(df)