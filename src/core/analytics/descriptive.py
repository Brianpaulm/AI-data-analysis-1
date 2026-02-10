import pandas as pd

def describe(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all")
