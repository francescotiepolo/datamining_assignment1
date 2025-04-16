def normalize_column(series, invert=False): # normalize (and invert if needed) a column
    min_val = series.min()
    max_val = series.max()
    norm = (series - min_val) / (max_val - min_val) if max_val != min_val else series - min_val
    if invert:
        norm = 1 - norm
    return norm

def sleep_deviation(bedtime, ideal=22.5): # Compute the deviation from ideal bedtime (in hours)
    diff = abs(bedtime - ideal)
    return min(diff, 24 - diff)