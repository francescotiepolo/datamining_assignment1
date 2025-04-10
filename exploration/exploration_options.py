#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import os
dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
parent = dir + ".." + os.path.sep
df = pd.read_csv(parent + "ODI-2025-parsed.csv",sep=";")

def pie_chart(df: pd.DataFrame, column: str, name: str):
    data = []
    keys = []
    for i, row in df.iterrows():
        key = row[column]
        if key in keys:
            data[keys.index(key)] += 1
        else:
            keys.append(key)
            data.append(1)
    plt.clf()
    plt.pie(data, labels=keys, autopct='%1.1f%%')
    name = name.replace(" ", "_")
    plt.savefig(dir + f"pie_chart_{name}.pdf")

def course_pie_chart(df: pd.DataFrame, name: str):
    pie_chart(df, f"Have you taken a course on {name}?", name)

def machine_learning(df: pd.DataFrame):
    course_pie_chart(df, "machine learning")

def information_retrieval(df: pd.DataFrame):
    course_pie_chart(df, "information retrieval")

def statistics(df: pd.DataFrame):
    course_pie_chart(df, "statistics")

def databases(df: pd.DataFrame):
    course_pie_chart(df, "databases")

def gender(df: pd.DataFrame):
    pie_chart(df, "What is your gender?", "gender")

machine_learning(df)
information_retrieval(df)
statistics(df)
databases(df)
gender(df)