#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
parent = dir + ".." + os.path.sep
df = pd.read_csv(parent + "csv_files" + os.path.sep + "filled.csv")

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
    plt.plot(column)
    plt.pie(data, labels=keys, autopct='%1.1f%%')
    name = name.replace(" ", "_")
    plt.savefig(dir + f"pie_chart_{name}.pdf")

def good_day(df: pd.DataFrame):
    new = {"What makes a good day for you?": df["category_goodday_1"].to_list()}
    new["What makes a good day for you?"].extend(df["category_goodday_2"].tolist())
    new["What makes a good day for you?"] = list(map(lambda x: x if x != "" else "empty", new["What makes a good day for you?"]))
    pie_chart(pd.DataFrame(new), "What makes a good day for you?", "goodday")

def time_to_bed(df: pd.DataFrame):
    labels = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00",
              "10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00",
              "20:00","21:00","22:00","23:00"]
    counts = [0] * len(labels)
    data = df["Parsed Time you went to bed Yesterday"].to_list()
    data = list(map(lambda x: int(x.split(":")[0]), data))
    for hour in data:
        temp = str(hour) if hour > 9 else f"0{hour}"
        counts[labels.index(f"{temp}:00")] += 1
    
    plt.clf()
    plt.bar(labels, counts)
    plt.savefig(dir + "hist_bed.pdf")

good_day(df)
time_to_bed(df)