# src/utils/pii_detector.py
import re
import pandas as pd
from typing import List, Dict, Any

# conservative regex patterns for MVP
PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone_eu": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{2,4}[-.\s]?){2,4}\d{2,4}\b"),
    "ssn_like": re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"),  # US-ish, keep conservative
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
}

def detect_pii_in_series(s: pd.Series, sample_n: int = 500) -> Dict[str, Any]:
    """
    Returns a dict: { pii_type: { 'count': int, 'examples': [..] } }
    Works on sampled text for speed.
    """
    text = s.astype(str)
    if len(text) > sample_n:
        text = text.sample(sample_n, random_state=42)
    joined = " ".join(text.tolist())
    results = {}
    for name, regex in PATTERNS.items():
        matches = regex.findall(joined)
        if matches:
            unique = list(dict.fromkeys(matches))[:10]
            results[name] = {"count_sample": len(matches), "examples": unique}
    return results

def detect_pii_in_dataframe(df: pd.DataFrame, cols: List[str] = None) -> pd.DataFrame:
    cols = cols or df.columns.tolist()
    rows = []
    for col in cols:
        col_result = detect_pii_in_series(df[col])
        rows.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "pii_found": bool(col_result),
            "pii_details": col_result
        })
    return pd.DataFrame(rows)
