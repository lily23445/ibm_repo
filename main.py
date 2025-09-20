from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import math
import pandas as pd
from datetime import datetime
import json
from db import engine, legacy_tabular, legacy_commands

# Import your parsers
from parsers.detect import detect_type
from parsers.flat_parser import parse_flat
from parsers.db2_parser import parse_db2
from parsers.green_parser import parse_green

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to clean NaN/inf
def clean_value(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v

@app.post("/upload-legacy")
async def upload_legacy(file: UploadFile = File(...)):
    raw = await file.read()
    legacy_type = detect_type(file.filename, raw)

    # Parse based on type
    if legacy_type in ["flat", "db2"]:  # tabular
        parsed = parse_flat(raw) if legacy_type == "flat" else parse_db2(raw)
        df = pd.DataFrame(parsed)
        cleaned_rows = [{k: clean_value(v) for k, v in row.items()} for row in parsed]

        # Store each row as JSON
        with engine.connect() as conn:
            for row in cleaned_rows:
                stmt = legacy_tabular.insert().values(
                    filename=file.filename,
                    upload_time=datetime.now(),
                    row_data=row
                )
                conn.execute(stmt)
            conn.commit()

        return JSONResponse({
            "filename": file.filename,
            "type": legacy_type,
            "rows_stored": len(parsed),
            "preview": cleaned_rows[:5]  # show first 5 rows
        })

    else:  # green-screen or non-tabular
        parsed = parse_green(raw)
        cleaned = [{k: clean_value(v) for k, v in row.items()} for row in parsed]

        # Store commands as JSON array
        with engine.connect() as conn:
            stmt = legacy_commands.insert().values(
                filename=file.filename,
                upload_time=datetime.now(),
                commands=cleaned
            )
            conn.execute(stmt)
            conn.commit()

        return JSONResponse({
            "filename": file.filename,
            "type": legacy_type,
            "rows_stored": len(parsed),
            "preview": cleaned
        })
