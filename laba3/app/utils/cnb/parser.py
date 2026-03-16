import re
from datetime import date
from decimal import Decimal


def parse_daily_date(first_line: str) -> date | None:
    match = re.match(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", first_line.strip())
    if not match:
        return None
    day, mon_str, year = match.groups()
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    try:
        month = months.index(mon_str) + 1
    except ValueError:
        return None
    return date(int(year), month, int(day))


def parse_daily_rates(
    text: str, currencies_filter: list[str] | None = None
) -> list[tuple[date, str, Decimal]]:
    lines = text.strip().splitlines()
    if len(lines) < 3:
        return []
    rate_date = parse_daily_date(lines[0])
    if not rate_date:
        return []
    header = lines[1]
    if "Code" not in header or "Rate" not in header or "Amount" not in header:
        return []
    result: list[tuple[date, str, Decimal]] = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) < 5:
            continue
        try:
            amount = int(parts[2])
            code = parts[3].strip()
            rate = Decimal(parts[4].replace(",", "."))
        except (ValueError, IndexError):
            continue
        if amount <= 0:
            continue
        if currencies_filter is not None and code not in currencies_filter:
            continue
        rate_per_unit = rate / amount
        result.append((rate_date, code, rate_per_unit))
    return result


def parse_year_header(header_line: str) -> list[tuple[str, int]]:
    parts = header_line.strip().split("|")
    if not parts or parts[0] != "Date":
        return []
    result: list[tuple[str, int]] = []
    for col in parts[1:]:
        col = col.strip()
        match = re.match(r"(\d+)\s+([A-Z]{3})\s*$", col, re.IGNORECASE)
        if match:
            amount = int(match.group(1))
            code = match.group(2).upper()
            result.append((code, amount))
        else:
            result.append(("", 1))
    return result


def parse_year_rates(
    text: str, currencies_filter: list[str] | None = None
) -> list[tuple[date, str, Decimal]]:
    lines = text.strip().splitlines()
    if len(lines) < 2:
        return []
    header_columns = parse_year_header(lines[0])
    if not header_columns:
        return []
    result: list[tuple[date, str, Decimal]] = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) != len(header_columns) + 1:
            continue
        try:
            d, m, y = parts[0].split(".")
            rate_date = date(int(y), int(m), int(d))
        except (ValueError, IndexError):
            continue
        for i, (code, amount) in enumerate(header_columns):
            if not code or (currencies_filter is not None and code not in currencies_filter):
                continue
            idx = i + 1
            if idx >= len(parts):
                continue
            try:
                raw = parts[idx].replace(",", ".")
                rate_for_amount = Decimal(raw)
            except (ValueError, IndexError):
                continue
            if amount <= 0:
                continue
            rate_per_unit = rate_for_amount / amount
            result.append((rate_date, code, rate_per_unit))
    return result
