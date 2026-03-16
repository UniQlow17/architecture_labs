def normalize_currencies(cur: list[str] | str) -> list[str]:
    if isinstance(cur, str):
        return [c.strip().upper() for c in cur.split(",") if c.strip()]
    result = []
    for c in cur:
        if not c or not str(c).strip():
            continue
        for part in str(c).strip().split(","):
            if part.strip():
                result.append(part.strip().upper())
    return result
