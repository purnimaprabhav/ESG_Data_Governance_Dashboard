# tests/test_pii_detector.py
import pandas as pd
from src.utils.pii_detector import detect_pii_in_dataframe

def test_pii_detection_sample():
    df = pd.DataFrame({
        "email_col": ["a@a.com", "b@b.org"],
        "nosense": ["x", "y"],
        "phone": ["+33 6 12 34 56 78", "1234567890"]
    })
    res = detect_pii_in_dataframe(df)
    assert res[res.column == "email_col"].pii_found.values[0] is True
    assert res[res.column == "nosense"].pii_found.values[0] is False
