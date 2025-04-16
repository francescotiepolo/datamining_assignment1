#!/usr/bin/python3
import pandas as pd
import os
from time_parse import time_parse
from number_parse import approximate_parse, stress_parse, sports_parse, random_number_parse

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + "csv_files/ODI-2025.csv",sep=";")
df = approximate_parse(df)
df = stress_parse(df)
df = sports_parse(df)
df = random_number_parse(df)
df = time_parse(df)

# Convert times written as 12.5 to 0.5 (both indicates half past midnight, but the 0.5 is in 24h format)
df["Parsed Time you went to bed Yesterday"] = pd.to_numeric(df["Parsed Time you went to bed Yesterday"], errors="coerce")
mask = (df["Parsed Time you went to bed Yesterday"] >= 12) & (df["Parsed Time you went to bed Yesterday"] < 13)
df.loc[mask, "Parsed Time you went to bed Yesterday"] = df.loc[mask, "Parsed Time you went to bed Yesterday"] - 12

df.to_csv(dir + "csv_files/ODI-2025-parsed.csv",sep=";")