def parse_green(raw: bytes):
    text = raw.decode()
    lines = text.strip().splitlines()
    return [{"command": l} for l in lines]
