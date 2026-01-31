from fastapi import FastAPI, UploadFile, File
import pandas as pd
import numpy as np
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def safe_rms(series):
    return float(np.sqrt(np.mean(series ** 2)))

@app.post("/upload-and-predict")
async def upload_and_predict(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(path)
    cols = set(df.columns)

    result = {
        "used_parameters": [],
        "missing_parameters": [],
    }

    for c in ["vin","vout","current","phase","freq","time"]:
        if c in cols:
            result["used_parameters"].append(c)
        else:
            result["missing_parameters"].append(c)

    prediction = "UNKNOWN"
    confidence = 0.3

    # ---- LOGIC 1: vin vout ----
    if "vin" in cols and "vout" in cols:
        vin_rms = safe_rms(df["vin"])
        vout_rms = safe_rms(df["vout"])
        att = vout_rms / vin_rms

        result["vin_rms"] = vin_rms
        result["vout_rms"] = vout_rms
        result["attenuation"] = att

        if att < 0.7:
            prediction = "HEALTHY CIRCUIT"
            confidence = 0.9
        else:
            prediction = "FAULTY CIRCUIT (NO ATTENUATION)"
            confidence = 0.85

    # ---- LOGIC 2: current ----
    elif "current" in cols:
        i_rms = safe_rms(df["current"])
        result["current_rms"] = i_rms

        if i_rms < 1e-6:
            prediction = "OPEN CIRCUIT"
            confidence = 0.95
        else:
            prediction = "CIRCUIT CONNECTED"
            confidence = 0.7

    # ---- LOGIC 3: phase ----
    elif "phase" in cols:
        phase_mean = float(df["phase"].mean())
        result["phase_mean"] = phase_mean

        if abs(phase_mean) > 30:
            prediction = "LOWPASS BEHAVIOR"
            confidence = 0.75
        else:
            prediction = "NON-LOWPASS CIRCUIT"
            confidence = 0.6

    return {
        "file": file.filename,
        "prediction": prediction,
        "confidence": confidence,
        "details": result
    }
