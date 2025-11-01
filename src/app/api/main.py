from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os
from src.utils.pii_detector import detect_pii_in_dataframe
from ydata_profiling import ProfileReport

app = FastAPI(title="EIB Data Governance Suite")

@app.post("/analyze/")
async def analyze_csv(file: UploadFile = File(...)):
    try:
        # Save uploaded CSV temporarily
        input_path = f"data/{file.filename}"
        output_dir = "data/output"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Load and analyze CSV
        df = pd.read_csv(input_path)
        pii_results = detect_pii_in_dataframe(df)

        # Save PII report
        pii_path = os.path.join(output_dir, "pii_report.csv")
        pii_results.to_csv(pii_path, index=False)

        # Generate profile report
        profile = ProfileReport(df, title="Dataset Profile", explorative=True)
        profile_path = os.path.join(output_dir, "profile_report.html")
        profile.to_file(profile_path)

        return {
            "message": "Analysis complete",
            "pii_report": pii_path,
            "profile_report": profile_path
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
