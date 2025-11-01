# src/app/demo_cli.py
import argparse
import pandas as pd
from pathlib import Path
from src.utils.pii_detector import detect_pii_in_dataframe
from src.utils.profiler import quick_profile, basic_metrics

def run(filepath: str, output_dir: str = "data/output"):
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(filepath)
    print("Loaded:", filepath)
    print("Basic metrics:", basic_metrics(df))

    profile = quick_profile(df, title="EIB Project Data Profiling")
    profile.to_file(p / "profile_report.html")
    print("Saved profile_report.html")

    pii_df = detect_pii_in_dataframe(df)
    pii_df.to_csv(p / "pii_report.csv", index=False)
    print("Saved pii_report.csv")
    print(pii_df[pii_df.pii_found])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default="data/output")
    args = parser.parse_args()
    run(args.csv, args.out)
