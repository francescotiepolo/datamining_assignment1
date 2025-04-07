import pandas as pd
import random
import math

def approximate_parse(df: pd.DataFrame) -> pd.DataFrame:
    df["Parsed How many students do you estimate there are in the room?"] = df["How many students do you estimate there are in the room?"]
    whitelist_set = set("0123456789.-")
    samples_needed = []
    guess = []
    for i, row in df.iterrows():
        parsed: str = str(row["Parsed How many students do you estimate there are in the room?"]).strip().lower()
        parsed = ''.join([c for c in parsed if c in whitelist_set]).strip()
        num = 0
        if len(parsed) == 0:
            samples_needed.append(i)
        elif "-" in parsed:
            parts = parsed.split("-")
            if len(parts[0]) == 0: #We have a negative number
                samples_needed.append(i)
            else:
                average = (float(parts[1]) - float(parts[0]))/2
                num = str(round(average))
                guess.append(num)
        elif "*" in parsed:
            parts = parsed.split("*")
            num = math.prod(map(lambda x: int(x), parts))
            guess.append(num)
        else:
            num = int(parsed)
            if num < 0 or num > 560:
                samples_needed.append(i)
            else:
                guess.append(num)
        df.at[i, "Parsed How many students do you estimate there are in the room?"] = num

    for i in samples_needed:
        df.at[i, "Parsed How many students do you estimate there are in the room?"] = random.choice(guess)
    return df

def stress_parse(df: pd.DataFrame) -> pd.DataFrame:
    df["Parsed What is your stress level (0-100)?"] = df["What is your stress level (0-100)?"]
    whitelist_set = set("0123456789.-")
    samples_needed = []
    random_number = []
    for i, row in df.iterrows():
        parsed: str = str(row["Parsed What is your stress level (0-100)?"]).strip().lower()
        parsed = ''.join([c for c in parsed if c in whitelist_set]).strip()
        try:
            number = float(parsed)
            if number < 0.0 or number > 100.0:
                samples_needed.append(i)
            else:
                df.at[i, "Parsed What is your stress level (0-100)?"] = str(number)
                random_number.append(str(number))
        except:
            samples_needed.append(i)

    for i in samples_needed:
        df.at[i, "Parsed What is your stress level (0-100)?"] = random.choice(random_number)
    return df

def sports_parse(df: pd.DataFrame) -> pd.DataFrame:
    df["Parsed How many hours per week do you do sports (in whole hours)?"] = df["How many hours per week do you do sports (in whole hours)? "]
    whitelist_set = set("0123456789.-")
    samples_needed = []
    sports = []
    for i, row in df.iterrows():
        parsed: str = str(row["Parsed How many hours per week do you do sports (in whole hours)?"]).strip().lower()
        parsed = ''.join([c for c in parsed if c in whitelist_set]).strip()
        num = 0
        if len(parsed) == 0:
            samples_needed.append(i)
        elif "-" in parsed:
            parts = parsed.split("-")
            average = (float(parts[1]) - float(parts[0]))/2
            num = str(round(average))
            sports.append(num)
        else:
            num = float(parsed)
            if num < 0:
                samples_needed.append(i)
            else:
                sports.append(num)
        df.at[i, "Parsed How many hours per week do you do sports (in whole hours)?"] = str(num)

    for i in samples_needed:
        df.at[i, "Parsed How many hours per week do you do sports (in whole hours)?"] = random.choice(str(sports))
    return df