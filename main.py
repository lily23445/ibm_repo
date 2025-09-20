from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import math

# Import your parsers
from parsers.detect import detect_type
from parsers.flat_parser import parse_flat
from parsers.db2_parser import parse_db2
from parsers.green_parser import parse_green

app = FastAPI()

# -------------------
# Enable CORS (for testing)
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Helper to clean NaN/inf
# -------------------
def clean_value(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v

# -------------------
# Upload endpoint
# -------------------
@app.post("/upload-legacy")
async def upload_legacy(file: UploadFile = File(...)):
    raw = await file.read()
    legacy_type = detect_type(file.filename, raw)

    # Parse based on type
    if legacy_type == "flat":
        parsed = parse_flat(raw)
    elif legacy_type == "db2":
        parsed = parse_db2(raw)
    else:
        parsed = parse_green(raw)

    # Clean NaN/inf for JSON compliance
    cleaned = [{k: clean_value(v) for k, v in row.items()} for row in parsed]  # all rows


    return JSONResponse(content={"type": legacy_type, "preview": cleaned})
