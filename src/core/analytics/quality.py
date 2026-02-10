import pandas as pd

def data_quality_score(df: pd.DataFrame) -> float:
    total = df.size
    missing = df.isna().sum().sum()
    return round(1 - (missing / total), 4) if total else 0.0
