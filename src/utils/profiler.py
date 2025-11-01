# src/utils/profiler.py
import pandas as pd
from ydata_profiling import ProfileReport

def quick_profile(df: pd.DataFrame, title: str = "Profile", minimal: bool = True):
    """
    Generates a ydata-profiling report object (viewable in notebook or saved HTML).
    """
    profile = ProfileReport(df, title=title, minimal=minimal)
    return profile

def basic_metrics(df: pd.DataFrame) -> dict:
    n = len(df)
    metrics = {"rows": n, "columns": df.shape[1], "missing_per_column": df.isna().sum().to_dict()}
    return metrics
