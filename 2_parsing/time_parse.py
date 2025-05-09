import pandas as pd
import re

def ampm_to_24(hour, am):
    if am:
        if hour == "12":
            return "00"
        else:
            return hour
    else:
        if hour == "12":
            return hour
        else:
            return str(int(hour) + 12)

def time_parse(df: pd.DataFrame) -> pd.DataFrame:
    df["Parsed Time you went to bed Yesterday"] = df["Time you went to bed Yesterday"]
    whitelist_set = set("0123456789amp :-.hu")
    samples_needed = []
    for i, row in df.iterrows():
        parsed: str = row["Parsed Time you went to bed Yesterday"].strip().lower()
        if "midnight" in parsed:
            df.at[i,"Parsed Time you went to bed Yesterday"] = 0.0
            continue
        parsed = ''.join([c for c in parsed if c in whitelist_set]).strip()
        if re.match("^((2[0-4])|((0|1)\d))([0-6]\d)$", parsed) is not None:
            parsed = f"{parsed[:2]}:{parsed[-2:]}"
        elif re.match("^((2[0-4])|((0|1)\d))(:|\.|-|h|u)([0-6]\d)$", parsed) is not None:
            parsed = parsed.replace(".", ":").replace("-", ":").replace("h", ":").replace("u", ":")
        elif re.match("^\d(:|\.|-|h|u)([0-6]\d)$", parsed) is not None:
            parsed = f"0{parsed}".replace(".", ":").replace("-", ":").replace("h", ":").replace("u", ":")
        elif re.match("^(2[0-4])|((0|1)\d)$", parsed) is not None:
            parsed = f"{parsed}:00"
        elif re.match("^\d$", parsed) is not None:
            parsed = f"0{parsed}:00"
        elif "am" in parsed or "pm" in parsed: #Handle am/pm
            am = "am" in parsed
            parsed = parsed.replace("am", "").replace("pm", "").strip()
            if re.match("^((2[0-4])|((0|1)\d))([0-6]\d)$", parsed) is not None:
                parsed = f"{parsed[:2]}:{parsed[-2:]}"
            elif re.match("^((2[0-4])|((0|1)\d))(:|\.|-|h|u)([0-6]\d)$", parsed) is not None:
                parsed = parsed.replace(".", ":").replace("-", ":").replace("h", ":").replace("u", ":")
            elif re.match("^\d(:|\.|-|h|u)([0-6]\d)$", parsed) is not None:
                parsed = f"0{parsed}".replace(".", ":").replace("-", ":").replace("h", ":").replace("u", ":")
            elif re.match("^(2[0-4])|((0|1)\d)$", parsed) is not None:
                parsed = f"{parsed}:00"
            elif re.match("^\d$", parsed) is not None:
                parsed = f"0{parsed}:00"
            else:
                samples_needed.append(i)
                continue
            parts = parsed.split(":")
            parsed = f"{ampm_to_24(parts[0], am)}:{parts[1]}"
        else:
            samples_needed.append(i)
            continue
        split = parsed.split(":")
        hour = float(split[0])
        minute = float(split[1])/60.0
        df.at[i,"Parsed Time you went to bed Yesterday"] = hour + minute

    for i in samples_needed:
        df.at[i, "Parsed Time you went to bed Yesterday"] = ""
    return df