#!/usr/bin/python3
import pandas as pd
from time_parse import time_parse
from number_parse import approximate_parse, stress_parse, sports_parse

ignore = [239,244]

df = pd.read_csv("./ODI-2025.csv",sep=";")
df = df.drop(ignore)
df = approximate_parse(df)
df = time_parse(df)
df = stress_parse(df)
df = sports_parse(df)
df.to_csv("./ODI-2025-parsed.csv",sep=";")