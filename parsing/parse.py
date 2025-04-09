#!/usr/bin/python3
import pandas as pd
import os
from time_parse import time_parse
from number_parse import approximate_parse, stress_parse, sports_parse, random_number_parse

ignore = [239,244]

dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep
df = pd.read_csv(dir + "ODI-2025.csv",sep=";")
df = df.drop(ignore)
df = approximate_parse(df)
df = stress_parse(df)
df = sports_parse(df)
df = random_number_parse(df)
df = time_parse(df)
df.to_csv(dir + "ODI-2025-parsed.csv",sep=";")