import pandas as pd
from io import BytesIO

def parse_db2(raw: bytes):
    df = pd.read_csv(BytesIO(raw), dtype=str)
    
    # Replace NaN with pd.NA (works for all dtypes)
    df = df.fillna(pd.NA)

    # Optional: convert DB2 timestamp to ISO
    if "ORDER_DATE" in df.columns:
        df["ORDER_DATE"] = df["ORDER_DATE"].str.replace("-00.00.00", "")

    return df.to_dict(orient="records")
