import pandas as pd
from io import StringIO

def parse_flat(raw: bytes):
    text = raw.decode()
    df = pd.read_fwf(StringIO(text))  # fixed-width

    # Replace NaN with pd.NA
    df = df.fillna(pd.NA)

    return df.to_dict(orient="records")
