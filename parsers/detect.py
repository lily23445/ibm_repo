def detect_type(filename: str, data: bytes) -> str:
    name = filename.lower()
    if name.endswith(".csv"):
        return "db2"
    text = data.decode(errors="ignore")
    if "DSP" in text or "WRK" in text:
        return "green"
    return "flat"
